"""Cache official alternative photometry with source URLs and byte hashes."""
from pathlib import Path
import urllib.request,hashlib,json,datetime,sys
root=Path(__file__).resolve().parents[2]
code=sys.argv[1] if len(sys.argv)>1 else '910505103630'
assert code.isdigit() and len(code)==12
urls={ext:f'https://api.microservices.signify.com/api/configurator/v2/getPhotometricAssets/{ext}?id={code}&locale=en_AA' for ext in ['uld','ldt']}
urls['pdf']=f'https://www.signify.com/api/assets/v1/file/Signify/content/{code}_EU.en_AA.PROF.FP/Localized_commercial_leaflet_{code}_en_AA.pdf'
records=[]
for ext,url in urls.items():
 p=root/'02_References/Manufacturer'/f'{code}.{ext}'
 if p.exists():raise ValueError(f'Existing cache: {p}')
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
 with urllib.request.urlopen(req,timeout=60) as response:
  data=response.read();resolved=response.url;ctype=response.headers.get('Content-Type')
 if ext=='pdf':assert data.startswith(b'%PDF')
 if ext=='uld':assert data.startswith(bytes.fromhex('d0cf11e0a1b11ae1'))
 if ext=='ldt':assert b'RC461B' in data
 p.write_bytes(data)
 records.append({'path':str(p.relative_to(root)),'url':url,'resolved_url':resolved,'content_type':ctype,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
out=root/'02_References/Manufacturer'/f'{code}-sources.json'
out.write_text(json.dumps({'fetched_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'product_page':f'https://www.signify.com/global/prof/indoor-luminaires/recessed/philips-powerbalance-gen2/{code}_EU/product','assets':records},indent=2),encoding='utf-8')
print(json.dumps(records,indent=2))
