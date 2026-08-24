import os
from urllib.parse import quote_plus
from psycopg2 import IntegrityError, errors, connect
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool
from dotenv import load_dotenv

# Silently passes if no .env file exists in production
load_dotenv()

# def build_db_url():
#     db_url = os.getenv('DATABASE_URL')
    
#     if not db_url:
#         host = os.getenv('DB_HOST', '').strip()
#         if ':' in host:
#             host = host.split(':')[0]
            
#         port = os.getenv('DB_PORT', '5432').strip()
#         db = os.getenv('DB_NAME', 'appdb').strip()
#         user = os.getenv('DB_USER', 'dbadmin').strip()
#         raw_password = os.getenv('DB_PASSWORD', '').strip()
        
#         # URL-encode password to safely handle special characters (@, #, $, %, etc.)
#         password = quote_plus(raw_password) if raw_password else ''
        
#         if host and user and raw_password:
#             db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    
#     # Do not force SSL mode when tunneling via localhost
#     if db_url and 'localhost' not in db_url and '127.0.0.1' not in db_url:
#         if 'sslmode=' not in db_url:
#             separator = '&' if '?' in db_url else '?'
#             db_url = f"{db_url}{separator}sslmode=require"
            
#     return db_url
import os
from urllib.parse import quote_plus
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor


def build_db_url():
    db_url = os.getenv('DATABASE_URL', '').strip()

    if not db_url:
        host = os.getenv('DB_HOST', '').strip()
        if ':' in host:
            host = host.split(':')[0]

        port = os.getenv('DB_PORT', '5432').strip()
        db = os.getenv('DB_NAME', 'appdb').strip()
        user = os.getenv('DB_USER', 'dbadmin').strip()
        raw_password = os.getenv('DB_PASSWORD', '').strip()

        password = quote_plus(raw_password) if raw_password else ''

        if host and user and raw_password:
            db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"

    # Ensure it is a valid URI protocol before adding query parameters
    if db_url and db_url.startswith("postgresql://"):
        if 'localhost' not in db_url and '127.0.0.1' not in db_url:
            if 'sslmode=' not in db_url:
                separator = '&' if '?' in db_url else '?'
                db_url = f"{db_url}{separator}sslmode=require"
        return db_url

    return None


DATABASE_URL = build_db_url()

try:
    if DATABASE_URL:
        db_pool = ThreadedConnectionPool(1, 10, dsn=DATABASE_URL)
        print('PostgreSQL connection pool created successfully.')
    else:
        print('Error: No valid database credentials or DATABASE_URL provided.')
        db_pool = None
except Exception as e:
    print(f'Error creating PostgreSQL connection pool: {e}')
    db_pool = None


def init_db():
    if not db_pool:
        print("Database pool not initialized. Skipping init_db.")
        return

    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100),
                    phone VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn and db_pool:
            db_pool.putconn(conn)


def get_all_contacts():
    if not db_pool:
        return []
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM contacts ORDER BY id DESC;")
            return cur.fetchall()
    except Exception as e:
        print(f"Error fetching contacts: {e}")
        return []
    finally:
        if conn and db_pool:
            db_pool.putconn(conn)


def add_contact(name, email=None, phone=None):
    if not db_pool:
        return None
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO contacts (name, email, phone) VALUES (%s, %s, %s) RETURNING *;",
                (name, email, phone)
            )
            new_contact = cur.fetchone()
            conn.commit()
            return new_contact
    except Exception as e:
        print(f"Error adding contact: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn and db_pool:
            db_pool.putconn(conn)