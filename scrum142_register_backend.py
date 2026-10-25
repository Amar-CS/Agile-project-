# SCRUM-142: إنشاء حساب جديد (Registration Backend Logic)
# مستخرج من ملف server.py

import sqlite3
import secrets
import hashlib
import re

# 1. دالة التشفير (مهمة جداً لحماية كلمة المرور قبل حفظها)
def hp(p, s=None):
    '''دالة لتشفير كلمة المرور الجديدة باستخدام PBKDF2'''
    s = s or secrets.token_hex(8)
    return s + '$' + hashlib.pbkdf2_hmac('sha256', p.encode(), s.encode(), 150000).hex()

# 2. كود مسار إنشاء الحساب (API Endpoint: POST /api/register)
def register_route(c, b, s):
    # c: Database connection/cursor
    # b: Request Body (JSON)
    # s: Server response handler
    
    # استخراج البيانات من الطلب وتنظيفها
    n = str(b.get('name', '')).strip()
    em = str(b.get('email', '')).strip().lower()
    pw = str(b.get('pass', ''))
    phone = str(b.get('phone', ''))[:20]
    role = b.get('role')
    
    ROLES = ['موظف مبيعات', 'أمين مخزن', 'محاسب']
    
    # 1. التحقق من صحة البيانات (Validation)
    # التأكد من طول الاسم، صيغة الإيميل، طول الباسورد، وصحة الدور
    if len(n) < 3 or not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', em) or len(pw) < 6 or role not in ROLES: 
        raise ApiErr(400, 'بيانات التسجيل غير صحيحة')
        
    # 2. التحقق من عدم تكرار البريد الإلكتروني (Uniqueness)
    if c.execute('select 1 from users where email=?', (em,)).fetchone(): 
        raise ApiErr(409, 'هذا البريد مسجل بالفعل')
        
    # 3. حفظ المستخدم في قاعدة البيانات بحالة "قيد الانتظار" (pending)
    # لاحظ استخدام دالة hp(pw) لتشفير كلمة المرور قبل الحفظ
    c.execute(
        "insert into users(name,email,phone,pass,role,st) values(?,?,?,?,?,'pending')",
        (n, em, phone, hp(pw), role)
    )
    c.commit()
    
    # إرجاع رد بنجاح العملية
    return s.out(201, {'ok': True})
