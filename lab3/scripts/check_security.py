"""Run only against the local fixture; retain every request and response."""
from pathlib import Path
import subprocess, json, datetime
BASE = Path(__file__).resolve().parents[1]
CASES = [
 ('01-plain', '/../../../etc/passwd'),
 ('02-encoded-slashes', '/..%2F..%2F..%2Fetc%2Fpasswd'),
 ('03-double-dots', '/....//....//....//etc/passwd'),
 ('04-download-control', '/download?file=readme.txt'),
 ('05-download-traversal', '/download?file=../private/demo.txt'),
 ('06-download-encoded', '/download?file=%2e%2e%2fprivate%2fdemo.txt'),
 ('07-download-double-encoded', '/download?file=%252e%252e%252fprivate%252fdemo.txt'),
 ('08-safe-traversal', '/safe-download?file=../private/demo.txt'),
 ('09-safe-encoded', '/safe-download?file=%2e%2e%2fprivate%2fdemo.txt'),
 ('10-safe-control', '/safe-download?file=readme.txt'),
 ('11-environment', '/.env'), ('12-config', '/config.php'),
 ('13-backup', '/backup.sql'), ('14-bak', '/config.php.bak'),
 ('15-old', '/index.php.old'), ('16-backup-extension', '/site.backup'),
 ('17-admin', '/admin'), ('18-wordpress', '/wp-admin'),
 ('19-phpmyadmin', '/phpmyadmin'), ('20-directory', '/uploads/'),
 ('21-headers', '/'), ('22-baseline404', '/definitely-missing-9d2734')
]
rows=[]
for name, path in CASES:
    cmd=['curl','--path-as-is','--max-time','10','-sS','-i','http://127.0.0.1:8083'+path]
    r=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (BASE/'logs'/f'security-{name}.txt').write_text('$ '+' '.join(cmd)+'\n\n'+r.stdout+f'\n[exit code: {r.returncode}]\n')
    assert r.returncode==0, r.stdout
    status=int(r.stdout.splitlines()[0].split()[1])
    rows.append(dict(case=name,path=path,status=status,traversal_marker='LAB3_PATH_TRAVERSAL_CONFIRMED' in r.stdout))
(BASE/'logs/security-summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print(json.dumps(rows,ensure_ascii=False,indent=2))
assert [r['status'] for r in rows[:10]] == [404,404,404,200,200,200,404,403,403,200]
assert rows[4]['traversal_marker'] and rows[5]['traversal_marker']
print('All 22 requests recorded; vulnerable and fixed endpoint behavior verified.')
