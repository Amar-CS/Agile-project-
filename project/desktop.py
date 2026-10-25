#!/usr/bin/env python3
"""Loader Store - desktop launcher: starts the server and opens it in its own app window (Edge/Chrome --app)."""
import os,sys,shutil,socket,subprocess,threading,webbrowser
import server
def free_port(p=8000):
    for q in range(p,p+50):
        with socket.socket() as s:
            if s.connect_ex(('127.0.0.1',q))!=0: return q
    return p
def find_browser():
    if os.environ.get('LS_BROWSER'): return os.environ['LS_BROWSER']
    pf=[os.environ.get(k,'') for k in ('PROGRAMFILES','PROGRAMFILES(X86)','LOCALAPPDATA')]
    c=[os.path.join(b,r) for b in pf if b for r in (r'Microsoft\Edge\Application\msedge.exe',r'Google\Chrome\Application\chrome.exe')]
    c+=['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge']
    c+=[shutil.which(x) or '' for x in ('google-chrome','chromium','chromium-browser','microsoft-edge')]
    return next((x for x in c if x and os.path.exists(x)),None)
def main():
    server.init();port=free_port(int(os.environ.get('PORT',8000)));url=f'http://127.0.0.1:{port}'
    httpd=server.ThreadingHTTPServer(('127.0.0.1',port),server.H);threading.Thread(target=httpd.serve_forever,daemon=True).start()
    b=find_browser()
    if not b: print('لم يتم العثور على Edge/Chrome، سيتم الفتح في المتصفح الافتراضي. اقفل هذه النافذة لإيقاف البرنامج.');webbrowser.open(url);threading.Event().wait();return
    prof=os.path.join(os.path.dirname(server.DBP),'app-window')
    subprocess.call([b,f'--app={url}',f'--user-data-dir={prof}','--window-size=1366,820','--no-first-run','--no-default-browser-check'])
    httpd.shutdown()
if __name__=='__main__': main()
