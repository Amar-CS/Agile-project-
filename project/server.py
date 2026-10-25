#!/usr/bin/env python3
"""Loader Store - web server (Python stdlib only) + SQLite. Run: python server.py"""
import json,sqlite3,hashlib,secrets,os,re,datetime,mimetypes
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
import sys
FROZEN=getattr(sys,'frozen',False);B=os.path.dirname(os.path.abspath(__file__));STAT=os.path.join(getattr(sys,'_MEIPASS',B),'static')
DBP=os.path.join(os.environ.get('APPDATA',B),'LoaderStore','loader.db') if FROZEN else os.path.join(B,'data','loader.db')
ENT={'products':['code','n','c','q','min','cost','price'],'suppliers':['name','phone','addr','note'],'customers':['name','phone','bal'],
'purchases':['no','sup','date','total','st'],'payments':['no','party','type','amt','date'],'expenses':['item','cat','amt','date']}
NUM={'q','min','cost','price','bal','total','amt'};EMP={'products':'r','customers':'rw','invoices':'rw','product_images':'r'};ROLES=['موظف مبيعات','أمين مخزن','محاسب']
class ApiErr(Exception):
    def __init__(s,code,msg): s.code,s.msg=code,msg
def db():
    c=sqlite3.connect(DBP);c.row_factory=sqlite3.Row;return c
def hp(p,s=None):
    s=s or secrets.token_hex(8);return s+'$'+hashlib.pbkdf2_hmac('sha256',p.encode(),s.encode(),150000).hex()
def chk(p,h): return secrets.compare_digest(hp(p,h.split('$')[0]),h)
def init():
    os.makedirs(os.path.dirname(DBP),exist_ok=True);c=db()
    for t,cols in ENT.items():
        c.execute(f'create table if not exists {t}(id integer primary key autoincrement,'+','.join(f'"{k}" '+('real' if k in NUM else 'text') for k in cols)+')')
    c.executescript('''create table if not exists invoices(id integer primary key autoincrement,no text,cust text,date text,total real,disc real);
    create table if not exists invoice_items(id integer primary key autoincrement,inv_id integer references invoices(id),n text,q integer,price real);
    create table if not exists users(id integer primary key autoincrement,name text,email text unique,phone text,pass text,role text,st text default '');
    create table if not exists sessions(token text primary key,uid integer);
    create table if not exists product_images(product_id integer primary key,thumb text,feat text);''')
    if not c.execute('select 1 from users').fetchone():
        for n,e,r in (('مدير النظام','admin@loader.com','مدير'),('سارة - موظفة','staff@loader.com','موظف مبيعات')):
            c.execute('insert into users(name,email,pass,role) values(?,?,?,?)',(n,e,hp('123456'),r))
        for r in [('FL-1001','فلتر زيت المحرك','فلاتر',12,5,300,450),('HY-2002','سلك هيدروليك','هيدروليك',5,5,220,320),('TR-3003','تيل فرامل','فرامل',9,10,520,680),('AC-4004','مبرد زيت','تبريد',15,10,180,250),('BK-5005','بلف هيدروليك','هيدروليك',6,5,620,750),('BK-6006','جلبة جاروف','جاروف',20,5,120,180)]:
            c.execute('insert into products(code,n,c,q,"min",cost,price) values(?,?,?,?,?,?,?)',r)
        for r in [('شركة التوريدات العامة','01012345678','القاهرة - مدينة نصر','جودة عالية'),('مؤسسة قطع الغيار','01098765432','الجيزة - حدائق الأهرام','أسعار مناسبة'),('شركة المعدات الثقيلة','01122334455','السويس','مواعيد ممتازة')]:
            c.execute('insert into suppliers(name,phone,addr,note) values(?,?,?,?)',r)
        for r in [('شركة النيل','01111111111',0),('أحمد محمد','01222222222',1500),('مؤسسة الصحراء','01033333333',0),('علي خالد','01555555555',800),('محمود جمعة','01066666666',0)]:
            c.execute('insert into customers(name,phone,bal) values(?,?,?)',r)
        c.execute("insert into purchases(no,sup,date,total,st) values('PO-101','شركة التوريدات العامة','2026-10-09',21000,'تم الاستلام')")
        c.execute("insert into expenses(item,cat,amt,date) values('إيجار المحل','ثابتة',6000,'2026-10-01')")
    c.commit();c.close()
class H(BaseHTTPRequestHandler):
    def log_message(s,*a): pass
    def out(s,code,obj,cookie=None):
        b=json.dumps(obj,ensure_ascii=False).encode();s.send_response(code);s.send_header('Content-Type','application/json; charset=utf-8');s.send_header('Content-Length',str(len(b)))
        if cookie: s.send_header('Set-Cookie',cookie)
        s.end_headers();s.wfile.write(b)
    def me(s,c):
        t=None
        for p in s.headers.get('Cookie','').split(';'):
            k,_,v=p.strip().partition('=')
            if k=='sid': t=v
        return c.execute('select u.* from sessions s join users u on u.id=s.uid where s.token=?',(t,)).fetchone() if t else None
    def static(s):
        p=s.path.split('?')[0];p='/index.html' if p=='/' else p;f=os.path.normpath(os.path.join(STAT,p.lstrip('/')))
        if not f.startswith(STAT) or not os.path.isfile(f): s.send_response(404);s.end_headers();return
        b=open(f,'rb').read();s.send_response(200);s.send_header('Content-Type',(mimetypes.guess_type(f)[0] or 'text/plain')+'; charset=utf-8');s.send_header('Content-Length',str(len(b)));s.end_headers();s.wfile.write(b)
    def dispatch(s,m):
        if not s.path.startswith('/api/'): return s.static()
        n=int(s.headers.get('Content-Length') or 0)
        try: body=json.loads(s.rfile.read(n) or b'{}') if n else {}
        except Exception: return s.out(400,{'error':'بيانات غير صحيحة'})
        c=db()
        try: s.route(c,m,s.path[5:].split('?')[0].strip('/').split('/'),body)
        except ApiErr as e: s.out(e.code,{'error':e.msg})
        except Exception: s.out(500,{'error':'خطأ في الخادم'})
        finally: c.close()
    def do_GET(s): s.dispatch('GET')
    def do_POST(s): s.dispatch('POST')
    def do_PUT(s): s.dispatch('PUT')
    def do_DELETE(s): s.dispatch('DELETE')
    def route(s,c,m,P,b):
        e=P[0]
        if e=='login' and m=='POST':
            u=c.execute('select * from users where email=?',(str(b.get('email','')).lower(),)).fetchone()
            if not u or not chk(str(b.get('pass','')),u['pass']): raise ApiErr(401,'البريد أو كلمة المرور غير صحيحة')
            if u['st']=='pending': raise ApiErr(403,'حسابك قيد موافقة المدير')
            if (u['role']=='مدير')!=(b.get('role')=='manager'): raise ApiErr(403,'اختر نوع الدخول الصحيح (مدير / موظف)')
            t=secrets.token_hex(24);c.execute('insert into sessions values(?,?)',(t,u['id']));c.commit()
            return s.out(200,{'id':u['id'],'name':u['name'],'email':u['email'],'role':u['role']},f'sid={t}; HttpOnly; SameSite=Strict; Path=/')
        if e=='register' and m=='POST':
            n,em,pw=str(b.get('name','')).strip(),str(b.get('email','')).strip().lower(),str(b.get('pass',''))
            if len(n)<3 or not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$',em) or len(pw)<6 or b.get('role') not in ROLES: raise ApiErr(400,'بيانات التسجيل غير صحيحة')
            if c.execute('select 1 from users where email=?',(em,)).fetchone(): raise ApiErr(409,'هذا البريد مسجل بالفعل')
            c.execute("insert into users(name,email,phone,pass,role,st) values(?,?,?,?,?,'pending')",(n,em,str(b.get('phone',''))[:20],hp(pw),b['role']));c.commit();return s.out(201,{'ok':True})
        if e=='forgot' and m=='POST': return s.out(200,{'ok':True})
        u=s.me(c)
        if e=='logout': 
            c.execute('delete from sessions where uid=?',(u['id'],)) if u else 0;c.commit();return s.out(200,{'ok':True},'sid=; Max-Age=0; Path=/')
        if not u: raise ApiErr(401,'سجّل الدخول أولًا')
        mgr=u['role']=='مدير'
        if e=='me': return s.out(200,{'id':u['id'],'name':u['name'],'email':u['email'],'role':u['role']})
        if e=='users':
            if not mgr: raise ApiErr(403,'غير مسموح')
            if m=='GET': return s.out(200,[dict(r) | {'pass':None} for r in c.execute('select id,name,email,role,st from users order by id')])
            if m=='POST' and len(P)==3 and P[2]=='approve': c.execute("update users set st='' where id=?",(P[1],));c.commit();return s.out(200,{'ok':True})
            raise ApiErr(404,'غير موجود')
        if not mgr:
            pm=EMP.get(e)
            if not pm or (m!='GET' and pm=='r'): raise ApiErr(403,'ليس لديك صلاحية')
        if e=='product_images':
            if m=='GET': return s.out(200,[dict(r) for r in c.execute('select * from product_images')])
            if m=='PUT':
                th,ft=str(b.get('thumb',''))[:60000],str(b.get('feat',''))[:30000]
                if not th.startswith('data:image/') or not ft.startswith('['): raise ApiErr(400,'صورة غير صحيحة')
                c.execute('insert into product_images(product_id,thumb,feat) values(?,?,?) on conflict(product_id) do update set thumb=excluded.thumb,feat=excluded.feat',(P[1],th,ft));c.commit();return s.out(200,{'ok':True})
            if m=='DELETE': c.execute('delete from product_images where product_id=?',(P[1],));c.commit();return s.out(200,{'ok':True})
            raise ApiErr(405,'غير مسموح')
        if e=='invoices':
            if m=='GET': return s.out(200,[dict(r) for r in c.execute('select id,no,cust,date,total from invoices order by id desc')])
            if m=='POST': return s.invoice(c,b)
            raise ApiErr(405,'غير مسموح')
        if e not in ENT: raise ApiErr(404,'غير موجود')
        cols=ENT[e]
        if m=='GET': return s.out(200,[dict(r) for r in c.execute(f'select * from {e} order by id')])
        if m in('POST','PUT'):
            try: v=[(float(b[k]) if k in NUM else str(b[k])[:200]) for k in cols]
            except Exception: raise ApiErr(400,'تأكد من تعبئة كل الحقول بشكل صحيح')
            q=','.join(f'"{k}"' for k in cols)
            if m=='POST': c.execute(f'insert into {e}({q}) values({",".join("?"*len(cols))})',v)
            else: c.execute(f'update {e} set '+','.join(f'"{k}"=?' for k in cols)+' where id=?',v+[P[1]])
            c.commit();return s.out(200,{'ok':True})
        if m=='DELETE':
            if e=='products': c.execute('delete from product_images where product_id=?',(P[1],))
            c.execute(f'delete from {e} where id=?',(P[1],));c.commit();return s.out(200,{'ok':True})
    def invoice(s,c,b):
        items=b.get('items') or [];disc=max(0.0,float(b.get('disc') or 0))
        if not items: raise ApiErr(400,'أضف صنفًا واحدًا على الأقل')
        c.execute('begin immediate');sub=0;rows=[]
        for it in items:
            p=c.execute('select * from products where n=?',(it.get('n'),)).fetchone();q=int(it.get('q',0))
            if not p or q<1: raise ApiErr(400,'صنف غير صحيح')
            if p['q']<q: raise ApiErr(400,f"المتاح من {p['n']} هو {int(p['q'])} فقط")
            sub+=q*p['price'];rows.append((p['id'],p['n'],q,p['price']))
        total=sub-disc+round((sub-disc)*0.14)
        cur=c.execute("insert into invoices(no,cust,date,total,disc) values('',?,?,?,?)",(str(b.get('cust',''))[:100],datetime.date.today().isoformat(),total,disc));i=cur.lastrowid
        c.execute('update invoices set no=? where id=?',('SI-%04d'%i,i))
        for pid,n,q,pr in rows:
            c.execute('insert into invoice_items(inv_id,n,q,price) values(?,?,?,?)',(i,n,q,pr));c.execute('update products set q=q-? where id=?',(q,pid))
        c.commit();s.out(201,{'id':i,'no':'SI-%04d'%i,'total':total})
if __name__=='__main__':
    init();port=int(os.environ.get('PORT',8000));print(f'Loader Store running on http://127.0.0.1:{port}  (Ctrl+C to stop)')
    ThreadingHTTPServer(('127.0.0.1',port),H).serve_forever()
