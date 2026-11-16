"""Read-only inspection of the STEP records and included schema in native evo.

Independent small record inspector; no EvoParse code is copied. The public
EvoParse project motivated inspecting the native STEP graph, but has no verified
license in this review. No result data are synthesized or modified here.
"""
from pathlib import Path
import sys,zipfile,re,json,hashlib,xml.etree.ElementTree as ET
def split_fields(s):
 parts=[];start=0;depth=0;quoted=False;enum=False;i=0
 while i<len(s):
  c=s[i]
  if quoted:
   if c=="'":
    if i+1<len(s) and s[i+1]=="'":i+=1
    else:quoted=False
  elif enum:
   if c=='.':enum=False
  elif c=="'":quoted=True
  elif c=='.' and i+1<len(s) and s[i+1].isalpha():enum=True
  elif c=='(':depth+=1
  elif c==')':depth-=1
  elif c==',' and depth==0:parts.append(s[start:i].strip());start=i+1
  i+=1
 if quoted or enum or depth:raise ValueError('Unbalanced STEP record')
 parts.append(s[start:].strip());return parts
def read(path):
 path=Path(path);raw=path.read_bytes()
 with zipfile.ZipFile(path) as z:
  text=z.read('Project/ProjectData/ProjectData.dat').decode('utf-8-sig')
  schema=ET.fromstring(z.read('Project/ProjectData/ProjectData.xml'))
 names={e.attrib['Name']:[m.attrib['Name'] for m in sorted(e.findall('Member'),key=lambda x:int(x.attrib['IndexInObject']))] for e in schema}
 objects={}
 matches=list(re.finditer(r'^#(\d+) = (\w+) \((.*?)\);',text,re.M|re.S))
 if len(matches)!=len(re.findall(r'^#\d+ = ',text,re.M)):raise ValueError('Unrecognized record')
 for m in matches:
  line=m[0]
  n=int(m[1]);type_name=m[2];values=split_fields(m[3]);fields=names.get(type_name,[])
  if len(fields)!=len(values):raise ValueError(f'Schema mismatch #{n} {type_name}: {len(fields)} fields, {len(values)} values')
  objects[n]={'step_id':n,'type':type_name,'fields':dict(zip(fields,values)),'raw':line}
 return {'source':str(path.resolve()),'sha256':hashlib.sha256(raw).hexdigest(),'objects':objects}
if __name__=='__main__':
 d=read(sys.argv[1]); ids=[int(x) for x in sys.argv[2:]]
 for n,o in d['objects'].items():
  if n in ids or any(k in o['type'] for k in ['CalcGrid','CalculationGrid','UgrCalculation','CalculationSurface']):print(json.dumps(o,ensure_ascii=True))
