"""Readable vector figures derived solely from verified design/result datasets."""
from pathlib import Path
import json,math
from reportlab.graphics.shapes import Drawing,Polygon,Rect,Circle,String,Line,PolyLine
from reportlab.lib import colors
r=Path(__file__).resolve().parents[2];data=r/'05_Calculations/data'
load=lambda name:json.loads((data/name).read_text())
room=load('room-v1.json');furniture=load('furniture-proposal-v1.json');plan=load('snapped-layout-proposal-v3.json');controls=load('controls-proposal-v2.json');metrics={t['name']:t for t in load('review-40s-reopened-tasks-v4.json')['tasks']}
black=colors.black;blue=colors.HexColor('#326C8C');pale=colors.HexColor('#EDF2F4');grey=colors.HexColor('#777777')
def label(d,x,y,text,size=9,anchor='start',bold=False,color=black):d.add(String(x,y,text,fontName='Bold' if bold else 'Body',fontSize=size,textAnchor=anchor,fillColor=color))
def poly(d,coords,xy,fill,stroke=grey,width=.5):d.add(Polygon([v for p in coords for v in xy(*p[:2])],fillColor=fill,strokeColor=stroke,strokeWidth=width))
def outline(d,scale,ox,oy,desks=False,fixtures=False):
 xy=lambda x,y:(ox+x*scale,oy+y*scale)
 poly(d,room['contour'],xy,colors.white,black,.7)
 for c in room['obstacles']:
  x,y=xy(c['center_m'][0]-c['size_m'][0]/2,c['center_m'][1]-c['size_m'][1]/2);d.add(Rect(x,y,c['size_m'][0]*scale,c['size_m'][1]*scale,fillColor=grey,strokeColor=None))
 if desks:
  for desk in furniture['desks']:poly(d,desk['polygon_m'],xy,None,grey,.35)
 if fixtures:
  for f in plan['fixtures']:
   x,y=xy(*f['position_m'][:2]);side=.597*scale;d.add(Rect(x-side/2,y-side/2,side,side,fillColor=black,strokeColor=None))
 return xy

def layout_polar(width=451):
 d=Drawing(width,231);outline(d,5.4,3,37,True,True)
 label(d,3,219,'(a) Ceiling layout',10,bold=True)
 label(d,3,19,'186 luminaires; 600 mm ceiling grid',9)
 label(d,3,6,'Bench outlines show the proposed desks.',9)
 rows=(r/'02_References/Manufacturer/910505103638.ldt').read_text().splitlines();mc,ng=int(rows[3]),int(rows[5]);assert (mc,ng,int(rows[2]))==(180,91,4)
 vals=list(map(float,rows[42+mc+ng:]));assert len(vals)==46*91
 curves=[vals[:91],vals[45*91:46*91]];maxval=max(max(v) for v in curves);limit=math.ceil(maxval/200)*200
 cx,cy=350,179;radius=78
 label(d,275,219,'(b) Light distribution',10,bold=True)
 for value in range(200,limit+1,200):
  rad=value/limit*radius;pts=[]
  for a in range(-90,91,3):pts.extend([cx+rad*math.sin(math.radians(a)),cy-rad*math.cos(math.radians(a))])
  d.add(PolyLine(pts,strokeColor=colors.HexColor('#C5C5C5'),strokeWidth=.4));label(d,cx+4,cy-rad+2,str(value),8,color=grey)
 for angle in [-90,-60,-30,0,30,60,90]:
  x=cx+radius*math.sin(math.radians(angle));y=cy-radius*math.cos(math.radians(angle));d.add(Line(cx,cy,x,y,strokeColor=colors.HexColor('#C5C5C5'),strokeWidth=.4))
  if angle in [-60,0,60]:label(d,x,y-11,str(abs(angle))+' deg',8,'middle')
 for vals,col,dash in [(curves[0],blue,None),(curves[1],black,[3,2])]:
  pts=[]
  for a in range(-90,91):
   rad=vals[abs(a)]/limit*radius;pts.extend([cx+rad*math.sin(math.radians(a)),cy-rad*math.cos(math.radians(a))])
  d.add(PolyLine(pts,strokeColor=col,strokeWidth=1.1,strokeDashArray=dash))
 label(d,350,194,'Intensity (cd/klm)',9,'middle')
 for y,col,dash,txt in [(53,blue,None,'C0-C180'),(38,black,[3,2],'C90-C270')]:
  d.add(Line(282,y+3,304,y+3,strokeColor=col,strokeWidth=1.1,strokeDashArray=dash));label(d,310,y,txt,9)
 label(d,275,19,'Manufacturer LDT [3]',9)
 return d

def task_map(width=451):
 d=Drawing(width,245);xy=outline(d,7.15,4,23)
 def colour(v):
  t=max(0,min(1,(v-500)/250));return colors.Color(.94-.70*t,.87-.22*t,.62+.04*t)
 for desk in furniture['desks']:poly(d,desk['polygon_m'],xy,colour(metrics[desk['id']]['average_lx']),black,.35)
 for mark,name in [('A','Desk-021'),('B','Desk-084'),('C','Desk-018')]:
  desk=next(x for x in furniture['desks'] if x['id']==name);x,y=xy(*desk['centre_m'][:2]);d.add(Circle(x,y,7,fillColor=black,strokeColor=None));label(d,x,y-3,mark,9,'middle',True,colors.white)
 label(d,337,223,'Desk mean (lx)',9,bold=True)
 for i in range(40):d.add(Rect(337+i*2.6,199,2.7,11,fillColor=colour(500+i/39*250),strokeColor=None))

 for v in [500,600,700,750]:label(d,337+(v-500)/250*104,185,str(v),8,'middle')
 for y,mark,name,desc in [(154,'A','Desk-021','Lowest mean'),(107,'B','Desk-084','Lowest uniformity'),(60,'C','Desk-018','Highest glare')]:
  label(d,337,y,mark+'  '+name,9,bold=True);label(d,337,y-14,desc,8.5)
 label(d,4,7,'Each coloured rectangle represents one desk.',9)
 return d

def critical_desks(width=451):
 d=Drawing(width,139);left=81;right=307;scale=(right-left)/800
 label(d,left,126,'Maintained desk-average illuminance (lx)',9,bold=True)
 for value in [0,250,500,750]:
  x=left+value*scale;d.add(Line(x,25,x,111,strokeColor=colors.HexColor('#DDDDDD'),strokeWidth=.4));label(d,x,12,str(value),8,'middle')
 label(d,354,126,'Uo',9,'middle',True);label(d,414,126,'Max. UGR',9,'middle',True)
 for y,name in [(96,'Desk-021'),(65,'Desk-084'),(34,'Desk-018')]:
  t=metrics[name];label(d,3,y+1,name,9,bold=True);d.add(Rect(left,y-3,t['average_lx']*scale,16,fillColor=blue,strokeColor=None));label(d,left+t['average_lx']*scale+5,y+1,str(int(t['average_lx'])),9)
  label(d,354,y+1,f"{t['u0']:.2f}",10,'middle');label(d,414,y+1,f"{t['max_directional_ugr']:.1f}",10,'middle')
 x=left+500*scale;d.add(Line(x,25,x,116,strokeColor=black,strokeWidth=1,strokeDashArray=[3,2]));label(d,325,0,'Dashed line: 500 lx criterion',9,'end')
 return d

def zone_map(width=451):
 from shapely.geometry import shape
 d=Drawing(width,244);scale=7.0;ox=4;oy=23;xy=lambda x,y:(ox+x*scale,oy+y*scale)
 for z in controls['zones']:
  circulation='circulation' in z['activity'].lower();geom=z['polygon'];polys=geom['coordinates'] if geom['type']=='MultiPolygon' else [geom['coordinates']]
  for p in polys:poly(d,p[0],xy,colors.HexColor('#D4DDE1') if circulation else colors.HexColor('#F3F5F6'),grey,.6)
  center = shape(geom).centroid
  x, y = xy(center.x, center.y)
  # Centre the visible capitals and digits around the polygon's area centroid.
  label(d, x, y - 2.65, z['id'], 8, 'middle', True)
 for c in room['obstacles']:
  x,y=xy(c['center_m'][0]-c['size_m'][0]/2,c['center_m'][1]-c['size_m'][1]/2);d.add(Rect(x,y,c['size_m'][0]*scale,c['size_m'][1]*scale,fillColor=grey,strokeColor=None))
 poly(d,room['contour'],xy,None,black,.7)
 label(d,330,214,'Control zones',10,bold=True)
 for y,col,txt in [(189,'#F3F5F6','28 bench zones'),(167,'#D4DDE1','4 circulation zones')]:
  d.add(Rect(330,y,10,10,fillColor=colors.HexColor(col),strokeColor=grey,strokeWidth=.5));label(d,345,y+1,txt,9)
 for y,txt in [(135,'Each zone:'),(119,'manual on/off/dim'),(91,'Largest zone:'),(75,'46.67 sq. m')]:label(d,330,y,txt,9)
 label(d,4,7,'Z01-Z32: independent control areas; not electrical circuits.',9)
 return d


def calculation_heights(width=210):
 d=Drawing(width,142)
 label(d,8,132,'Calculation heights',10,bold=True)
 for z,name in [(2.8,'2.8 m  Ceiling'),(1.2,'1.2 m  UGR observer'),(.8,'0.8 m  Desk plane'),(0,'0.0 m  Floor')]:
  y=15+z*35;d.add(Line(10,y,55,y,strokeColor=black if z in [0,2.8] else blue,strokeWidth=.8,strokeDashArray=None if z in [0,2.8] else [3,2]));label(d,66,y-3,name,9)
 d.add(Line(10,15,10,113,strokeColor=grey,strokeWidth=.6))
 d.add(Rect(24,110,18,3,fillColor=black,strokeColor=None))
 d.add(Circle(35,57,3,fillColor=None,strokeColor=blue,strokeWidth=.8))
 return d
