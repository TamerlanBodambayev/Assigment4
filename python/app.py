from flask import Flask, render_template, request, flash
import mysql.connector
import bcrypt
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Конфигурация MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ЙФЯЧЫЦУВСМАКйфячыцувсмак7',
    'database': 'auth_demo'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Небезопасный вход (уязвимый к SQL-инъекциям)
@app.route('/insecure_login', methods=['GET', 'POST'])
def insecure_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # ⚠️ УЯЗВИМЫЙ КОД: прямая конкатенация строк
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            print(f"Выполняется запрос: {query}")  # Для демонстрации
            
            cursor.execute(query)
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result:
                return f"<h3>Добро пожаловать, {result[1]}!</h3><p>⚠️ Уязвимый вход успешен</p>"
            else:
                return "<h3>Неверные учетные данные</h3>"
                
        except Exception as e:
            return f"<h3>Ошибка: {str(e)}</h3>"
    
    return render_template('login.html', form_type='insecure')

# Безопасный вход
@app.route('/secure_login', methods=['GET', 'POST'])
def secure_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # ✅ БЕЗОПАСНЫЙ КОД: параметризованные запросы
            query = "SELECT id, username, password FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result and bcrypt.checkpw(password.encode('utf-8'), result[2].encode('utf-8')):
                return f"<h3>Добро пожаловать, {result[1]}!</h3><p>✅ Безопасный вход успешен</p>"
            else:
                return "<h3>Неверные учетные данные</h3>"
                
        except Exception as e:
            return f"<h3>Ошибка: {str(e)}</h3>"
    
    return render_template('login.html', form_type='secure')

@app.route('/')
def index():
    return '''
    <h1>Демонстрация безопасного кодирования</h1>
    <ul>
        <li><a href="/insecure_login">Небезопасный вход (SQL-инъекция)</a></li>
        <li><a href="/secure_login">Безопасный вход</a></li>
    </ul>
    '''

if __name__ == '__main__':
    app.run(debug=True)