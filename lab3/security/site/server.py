"""Intentionally vulnerable local training fixture. Never expose to a public network."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlsplit, parse_qs, unquote
import html
ROOT = Path('/app/public')
class Handler(BaseHTTPRequestHandler):
    server_version = 'LabTraining/1.0'
    sys_version = ''
    def reply(self, code, body, kind='text/html; charset=utf-8'):
        data = body.encode()
        self.send_response(code)
        self.send_header('Content-Type', kind)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def do_GET(self):
        u = urlsplit(self.path)
        path = unquote(u.path)
        if path in ('/download', '/safe-download'):
            name = parse_qs(u.query).get('file', ['readme.txt'])[0]
            target = (ROOT / name).resolve()
            if path == '/safe-download' and not target.is_relative_to(ROOT.resolve()):
                return self.reply(403, 'Forbidden: path outside public directory', 'text/plain')
            try: return self.reply(200, target.read_text(), 'text/plain; charset=utf-8')
            except (OSError, UnicodeError): return self.reply(404, 'Not found', 'text/plain')
        if path == '/':
            return self.reply(200, '<h1>Lab 3 — Local Security Training</h1><p>Isolated fixture. All data are synthetic.</p><ul><li><a href="/about">About</a></li><li><a href="/download?file=readme.txt">Download</a></li></ul>')
        if path == '/about': return self.reply(200, '<h1>About</h1><p>Training application for lab 3.</p>')
        if path == '/admin': return self.reply(403, 'Forbidden', 'text/plain')
        if path == '/uploads':
            self.send_response(301); self.send_header('Location', '/uploads/'); self.end_headers(); return
        if path == '/uploads/': return self.reply(200, '<h1>Index of /uploads/</h1><a href="/uploads/demo.txt">demo.txt</a>')
        exposed = { '/.env':'APP_ENV=training\nDEMO_TOKEN=NOT_A_REAL_SECRET\n', '/backup.sql':'-- SYNTHETIC TRAINING BACKUP\nCREATE TABLE demo (id INTEGER);\n', '/config.php.bak':'<?php // TRAINING ONLY; no real credentials ?>', '/uploads/demo.txt':'Public training file', '/robots.txt':'User-agent: *\nDisallow: /admin\n' }
        if path in exposed: return self.reply(200, exposed[path], 'text/plain')
        return self.reply(404, 'Not found', 'text/plain')
HTTPServer(('0.0.0.0', 8080), Handler).serve_forever()
