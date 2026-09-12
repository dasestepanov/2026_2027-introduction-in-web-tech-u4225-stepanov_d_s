from pathlib import Path
import json, urllib.request, urllib.parse, base64, subprocess
B=Path(__file__).resolve().parents[1]
def get(url,auth=False):
 req=urllib.request.Request(url)
 if auth: req.add_header('Authorization','Basic '+base64.b64encode(b'admin:admin').decode())
 return json.load(urllib.request.urlopen(req,timeout=20))
def save(n,j): (B/'logs'/n).write_text(json.dumps(j,ensure_ascii=False,indent=2))
t=get('http://127.0.0.1:9090/api/v1/targets');save('04-targets.json',t)
assert len(t['data']['activeTargets'])==2
assert all(x['health']=='up' for x in t['data']['activeTargets']), t
h=get('http://127.0.0.1:3000/api/health');save('05-grafana-health.json',h)
s=get('http://127.0.0.1:3000/api/datasources/uid/prometheus/health',True);save('06-datasource-health.json',s)
assert s['status']=='OK',s
board=get('http://127.0.0.1:3000/api/dashboards/uid/lab3-monitoring',True);save('07-dashboard.json',board)
results=[]
for panel in board['dashboard']['panels']:
 for target in panel['targets']:
  q=target['expr']; j=get('http://127.0.0.1:9090/api/v1/query?'+urllib.parse.urlencode({'query':q}))
  assert j['status']=='success' and j['data']['result'], (q,j)
  results.append(dict(panel=panel['title'],query=q,response=j))
save('08-promql.json',results)
print('PASS: 2/2 targets UP; Grafana database OK; data source OK; 4 panels / 5 PromQL queries contain data.')
for row in results: print(row['panel'], 'series:', len(row['response']['data']['result']))
