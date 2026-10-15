#!/usr/bin/env python3
"""Build a portable, offline-capable UI review board from a local JSON manifest."""
import argparse, hashlib, json, re, shutil
from pathlib import Path

SAFE_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.-]{0,95}$')
IMAGE_TYPES = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg'}

def build(manifest, output):
    source = manifest.resolve()
    raw = json.loads(source.read_text(encoding='utf-8'))
    for key in ('projectId', 'revision'):
        if not isinstance(raw.get(key), str) or not SAFE_ID.fullmatch(raw[key]):
            raise ValueError(f'{key} must be a stable ID: letters, numbers, dash, dot or underscore')
    entries = raw.get('entries')
    if not isinstance(entries, list) or not entries:
        raise ValueError('entries must be a non-empty list')
    pages, copies, seen = [], [], set()
    for item in entries:
        ident = str(item.get('id', ''))
        if not SAFE_ID.fullmatch(ident) or ident in seen:
            raise ValueError(f'Invalid or duplicate page ID: {ident}')
        seen.add(ident)
        title = item.get('title')
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f'{ident}: title is required')
        views = item.get('views')
        if views is None:
            views = [{'id': k, 'label': label, 'image': item[k]} for k, label in [('desktop','电脑端'),('tablet','平板端'),('mobile','手机端')] if item.get(k)]
        if not isinstance(views, list) or not views:
            raise ValueError(f'{ident}: at least one image view is required')
        normalized, view_ids = [], set()
        for view in views:
            vid = view.get('id', '')
            if not isinstance(vid, str) or not SAFE_ID.fullmatch(vid) or vid in view_ids:
                raise ValueError(f'{ident}: invalid or duplicate view ID')
            view_ids.add(vid)
            img = view.get('image')
            if not isinstance(img, str) or not img:
                raise ValueError(f'{ident}/{vid}: image path is required')
            path = (source.parent / img).resolve()
            if not path.is_relative_to(source.parent) or not path.is_file() or path.suffix.lower() not in IMAGE_TYPES:
                raise ValueError(f'{ident}/{vid}: image must be a local image inside manifest directory')
            name = f'{ident}-{vid}{path.suffix.lower()}'
            copies.append((path, name))
            normalized.append({'id': vid, 'label': str(view.get('label', vid)), 'image': name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        pages.append({'id':ident,'title':title,'note':str(item.get('note','')),'kind':str(item.get('kind','页面')),'views':normalized})
    data = {'schema':'frontend-ui-review-board/v1','projectId':raw['projectId'],'title':str(raw.get('title',raw['projectId'])),'revision':raw['revision'],'description':str(raw.get('description','逐页查看 UI，填写修改意见，再统一导出。')),'entries':pages}
    template = (Path(__file__).resolve().parent.parent/'assets/review.html').read_text(encoding='utf-8')
    if template.count('__REVIEW_DATA__') != 1:
        raise ValueError('Template must have exactly one data placeholder')
    embedded = json.dumps(data, ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    output.mkdir(parents=True, exist_ok=True)
    for path,name in copies:
        target=output/name
        if path != target.resolve(): shutil.copy2(path,target)
    (output/'index.html').write_text(template.replace('__REVIEW_DATA__',embedded),encoding='utf-8')
    (output/'review-manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'pages':len(pages),'images':len(copies),'output':str(output.resolve()),'projectId':data['projectId'],'revision':data['revision']},ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    build(args.manifest,args.out)
