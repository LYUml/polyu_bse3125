"""Prepare isolated native comparison inputs; only actual evo results are evidence."""
from pathlib import Path
import sys, json, zipfile, hashlib, re
from read_native_archive import read

source, target = map(Path, sys.argv[1:3])
variant = sys.argv[3]
assert variant in ('output90', 'reflectance') and not target.exists()
d = read(source)
active_prototype = next(o for o in d['objects'].values() if o['type']=='LuminairePrototype' and o['fields']['ObjectGuid']=="'76180ce0-f1c1-4543-860d-c8d94c1cf11b'")
dim_keys = {int(n) for o in d['objects'].values() if o['type']=='LuminaireGroupRepresentationData' for n in re.findall(r'#(\d+)',o['fields']['DimValues'])}
changes = []
with zipfile.ZipFile(source) as zi:
    text = zi.read('Project/ProjectData/ProjectData.dat').decode('utf-8-sig')
    for obj in d['objects'].values():
        f = dict(obj['fields'])
        if variant == 'output90' and obj['type'] == 'LuminaireGroupRepresentationData':
            assert re.fullmatch(r'\(\(#\d+, 1\.\)\)', f['DimValues'])
            f['DimValues'] = f['DimValues'].replace(', 1.)', ', 0.9)')
        elif variant == 'output90' and obj['step_id'] in dim_keys and obj['type']=='DimValueKey' and f['LuminairePrototypeId'] != active_prototype['fields']['ObjectId']:
            f['LuminairePrototypeId'] = active_prototype['fields']['ObjectId']
        elif variant == 'reflectance' and obj['type'] == 'MaterialParams' and 'Design white finish reflectance' in f['InternalName']:
            old = float(f['ColorLuminance'])
            assert abs(old-.8)<1e-6 or abs(old-.7)<1e-6
            new = .7 if abs(old-.8)<1e-6 else .5
            f['ColorLuminance'] = str(new)
            f['ColorBase'] = f'({new}, {new}, {new})'
            f['InternalName'] = f['DisplayName'] = f"'Sensitivity finish reflectance {new}'"
        else:
            continue
        row = f"#{obj['step_id']} = {obj['type']} (" + ', '.join(f.values()) + ');'
        assert text.count(obj['raw']) == 1
        text = text.replace(obj['raw'], row)
        changes.append({'type':obj['type'], 'id':obj['step_id'], 'before':obj['fields'], 'after':f})
    assert len(changes) in ([1,2] if variant == 'output90' else [2])
    with zipfile.ZipFile(target, 'x') as zo:
        for item in zi.infolist():
            if item.filename == 'Project/ScenegraphScene' or item.filename.startswith('Project/Results/'):
                continue
            zo.writestr(item, text.encode('utf-8-sig') if item.filename == 'Project/ProjectData/ProjectData.dat' else zi.read(item))
result = read(target)
assert d['sha256'] == hashlib.sha256(source.read_bytes()).hexdigest()
changed = {c['id'] for c in changes}
assert d['objects'].keys() == result['objects'].keys()
assert all(o == result['objects'][n] for n,o in d['objects'].items() if n not in changed)
record = {'status':'Prepared only; fresh native calculation and saved/reopened verification required', 'variant':variant, 'source':str(source.resolve()), 'source_sha256':d['sha256'], 'output':str(target.resolve()), 'output_sha256':result['sha256'], 'changes':changes, 'all_other_records_unchanged':True, 'cached_scene_and_results_removed':True}
target.with_suffix('.variant.json').write_text(json.dumps(record,indent=2))
print(json.dumps({k:v for k,v in record.items() if k!='changes'},indent=2))
