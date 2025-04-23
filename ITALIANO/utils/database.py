import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import logging

def init_db():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.database = DB_NAME

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT PRIMARY KEY,
                username VARCHAR(255),
                score INT DEFAULT 0
            )
        """)
        conn.commit()
        conn.close()
        logging.info("База данных успешно инициализирована.")
    except Exception as e:
        logging.error(f"Ошибка при инициализации базы данных: {e}")
        raise

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except Exception as e:
        logging.error(f"Ошибка при подключении к базе данных: {e}")
        raise

def get_user_score(user_id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT score FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return 0
    except Exception as e:
        logging.error(f"Ошибка при получении очков пользователя {user_id}: {e}")
        raise

def update_user_score(user_id, username, score_change): # Добавляем username в параметры
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        logging.info(f"Обновляем пользователя: user_id={user_id}, username={username}, score_change={score_change}") # Добавляем логирование

        cursor.execute("""
            INSERT INTO users (user_id, username, score) 
            VALUES (%s, %s, %s) 
            ON DUPLICATE KEY UPDATE 
            username = %s, 
            score = score + %s
        """, (user_id, username, score_change, username, score_change))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Ошибка при обновлении очков пользователя {user_id}: {e}")
        raise

def get_top_users():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, score FROM users ORDER BY score DESC LIMIT 10")
        results = cursor.fetchall()
        conn.close()
        top_users = []
        for result in results:
            user_id, username, score = result
            top_users.append({'user_id': user_id, 'username': username, 'score': score})
        logging.info(f"get_top_users returned: {top_users}") # Добавили логирование
        return top_users
    except Exception as e:
        logging.error(f"Ошибка при получении топ пользователей: {e}")
        raise