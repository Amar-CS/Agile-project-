# SCRUM-143: تسجيل الدخول (Login Backend Logic)
# مستخرج من ملف server.py

import sqlite3
import secrets
import hashlib

# 1. دوال التشفير والتحقق من كلمة المرور
def hp(p, s=None):
    '''دالة لتشفير كلمة المرور الجديدة'''
    s = s or secrets.token_hex(8)
    return s + '$' + hashlib.pbkdf2_hmac('sha256', p.encode(), s.encode(), 150000).hex()

def chk(p, h): 
    '''دالة للتحقق من تطابق كلمة المرور المدخلة مع المشفرة في قاعدة البيانات'''
    return secrets.compare_digest(hp(p, h.split('$')[0]), h)

# 2. كود مسار تسجيل الدخول (API Endpoint: POST /api/login)
# يتم تنفيذ هذا الكود عندما يرسل الـ Frontend طلب دخول
def login_route(c, b, s):
    # c: Database connection/cursor
    # b: Request Body (JSON)
    # s: Server response handler
    
    # استخراج الإيميل والباسورد من الطلب
    email = str(b.get('email', '')).lower()
    password = str(b.get('pass', ''))
    
    # البحث عن المستخدم في قاعدة البيانات
    u = c.execute('select * from users where email=?', (email,)).fetchone()
    
    # التحقق من وجود الحساب وصحة كلمة المرور باستخدام دالة chk
    if not u or not chk(password, u['pass']): 
        raise ApiErr(401, 'البريد أو كلمة المرور غير صحيحة')
    
    # التأكد أن الحساب مفعل وليس قيد الانتظار
    if u['st'] == 'pending': 
        raise ApiErr(403, 'حسابك قيد موافقة المدير')
        
    # التأكد من صحة نوع الدخول (مدير أم موظف)
    if (u['role'] == 'مدير') != (b.get('role') == 'manager'): 
        raise ApiErr(403, 'اختر نوع الدخول الصحيح (مدير / موظف)')
        
    # إنشاء جلسة آمنة (Session Token)
    t = secrets.token_hex(24)
    c.execute('insert into sessions values(?,?)', (t, u['id']))
    c.commit()
    
    # إرجاع بيانات المستخدم مع الـ Cookie الخاص بالجلسة
    return s.out(200, 
        {'id': u['id'], 'name': u['name'], 'email': u['email'], 'role': u['role']}, 
        f'sid={t}; HttpOnly; SameSite=Strict; Path=/'
    )
