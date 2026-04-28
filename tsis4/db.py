import psycopg2
from psycopg2 import sql
from datetime import datetime

DB_CONFIG = {
    "dbname": "snake_game",
    "user": "postgres",
    "password": "987654321",
    "host": "localhost",
    "port": "5432",
    "client_encoding": "utf8"
}

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="snake_game",
            user="postgres",
            password="987654321",
            host="localhost",
            port="5432",
            client_encoding='utf8'
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
    
def init_db():
    conn = get_connection() #initializes the database schema if it doesn't exist
    if not conn:
        return

    try:
        cur = conn.cursor() #create players table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
        """)
    
        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """) #game sessions table
        conn.commit()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Initialization error: {e}")
    finally:
        cur.close()
        conn.close()

def save_result(username, score, level):
    conn = get_connection()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING",
            (username,)
        )
        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        player_id = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
            (player_id, score, level)
        )
        conn.commit()
    except Exception as e:
        print(f"Database Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def get_leaderboard(limit=10):
    """Fetches the top scores from the database."""
    conn = get_connection()
    if not conn:
        return []

    try:
        cur = conn.cursor()
        query = """
            SELECT p.username, gs.score, gs.level_reached, gs.played_at 
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            ORDER BY gs.score DESC, gs.played_at DESC
            LIMIT %s
        """
        cur.execute(query, (limit,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def get_personal_best(username): #returns the highest score for a specific user
    conn = get_connection()
    if not conn:
        return 0

    try:
        cur = conn.cursor()
        query = """
            SELECT MAX(gs.score) 
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            WHERE p.username = %s
        """
        cur.execute(query, (username,))
        result = cur.fetchone()[0]
        return result if result is not None else 0
    except Exception as e:
        print(f"Error fetching personal best: {e}")
        return 0
    finally:
        cur.close()
        conn.close()