import mysql.connector
import bcrypt

# Конфигурация MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ЙФЯЧЫЦУВСМАКйфячыцувсмак7'
}

def setup_database():
    try:
        # Подключение к MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Создание базы данных
        cursor.execute("CREATE DATABASE IF NOT EXISTS auth_demo")
        cursor.execute("USE auth_demo")
        
        # Создание таблицы пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')
        
        # Очистка старых данных
        cursor.execute("DELETE FROM users")
        
        # Создание тестовых пользователей
        test_users = [
            ('admin', 'admin123'),
            ('user1', 'password123'),
            ('test', 'test123')
        ]
        
        for username, password in test_users:
            # Хеширование пароля с bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Вставка пользователя
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, hashed_password.decode('utf-8'))
            )
        
        # Также добавляем пользователя с простым паролем для демонстрации уязвимости
        cursor.execute("INSERT INTO users (username, password) VALUES ('vulnerable', 'simplepass')")
        
        conn.commit()
        print("✅ База данных создана успешно!")
        print("\nТестовые пользователи:")
        for username, password in test_users:
            print(f"  Логин: {username}, Пароль: {password}")
        print("  Логин: vulnerable, Пароль: simplepass (для демонстрации уязвимости)")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    setup_database()