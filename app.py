import os
import sqlite3
from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# دالة ذكية لتحديد مسار قاعدة البيانات بناءً على النظام (ويندوز أم قوقل كلاود)
def get_db_path():
    # إذا كان السيرفر يعمل على قوقل كلاود (لينكس)
    if os.name != 'nt':  
        return os.path.join('/tmp', 'database.db')
    # إذا كان يعمل محلياً على جهازك (ويندوز)
    else:  
        return 'database.db'

# إنشاء قاعدة البيانات والجدول
def init_db():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# المسار الرئيسي لعرض الصفحة وصندوق الإدخال
@app.route('/')
def home():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('SELECT name FROM users')
    all_rows = cursor.fetchall()
    conn.close()
    
    names_list_html = ""
    for row in all_rows:
        names_list_html += f"<li style='padding: 5px; background: #edf2f7; margin: 5px auto; width: 300px; border-radius: 5px;'>{row}</li>"
        
    if not names_list_html:
        names_list_html = "<p style='color: gray;'>لا توجد أسماء مسجلة بعد.</p>"

    return f"""
    <div style="text-align: center; margin-top: 50px; font-family: Arial, sans-serif; direction: rtl;">
        <h1 style="color: #2b6cb0;">سيرفر Flask المطور وقاعدة البيانات جاهز للرفع ☁️💾</h1>
        
        <form action="/add" method="POST" style="margin: 30px auto; padding: 20px; background: #f7fafc; width: 350px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <p style="margin-top: 0; color: #4a5568;"><b>أضف اسماً جديداً مباشرة:</b></p>
            <input type="text" name="username" placeholder="اكتب الاسم هنا..." required style="padding: 10px; width: 80%; border: 1px solid #cbd5e0; border-radius: 5px; font-size: 16px;"><br><br>
            <button type="submit" style="padding: 10px 20px; background: #2b6cb0; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; width: 86%;">حفظ في قاعدة البيانات</button>
        </form>
        
        <hr style="width: 50%; margin: 30px auto; border: 0; border-top: 1px solid #e2e8f0;">
        
        <h3>📋 الأسماء المسجلة حالياً:</h3>
        <ul style="list-style-type: none; padding: 0; font-size: 18px; color: #2d3748;">
            {names_list_html}
        </ul>
    </div>
    """

@app.route('/add', methods=['POST'])
def add_user():
    name_to_save = request.form.get('username')
    if name_to_save:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name) VALUES (?)', (name_to_save,))
        conn.commit()
        conn.close()
    return redirect(url_for('home'))

import os

# ... بقية كود الـ Flask وقاعدة البيانات الخاص بك ...

if __name__ == '__main__':
    app.run(port=8080)