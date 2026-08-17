import os
from psycopg2 import IntegrityError, errors
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

try:
    db_pool = SimpleConnectionPool(1, 5, dsn=DATABASE_URL)
    print('PostgreSQL connection pool created successfully.')
except Exception as e:
    print(f'Error creating PostgreSQL connection pool: {e}')
    db_pool = None


def get_db_connection():
    if db_pool:
        return db_pool.getconn()
    raise Exception('Database connection pool is not available.')


def release_db_connection(conn):
    if db_pool and conn:
        db_pool.putconn(conn)


def init_db():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    phone_number VARCHAR(20) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            conn.commit()
            print('Database initialised successfully.')
    except Exception as e:
        print(f'Failed to initialise database: {e}')
    finally:
        if conn:
            release_db_connection(conn)


def _query(query, params=None, fetchone=False, fetchall=False):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params or ())
            if not query.strip().lower().startswith('select'):
                conn.commit()
            if fetchone:
                return cur.fetchone()
            if fetchall:
                return cur.fetchall()
            return None
    finally:
        release_db_connection(conn)



def get_all_contacts():
    return _query(
        'SELECT id, first_name, last_name, phone_number, email, created_at FROM contacts ORDER BY created_at DESC',
        fetchall=True,
    )


def get_contact_by_id(contact_id):
    return _query(
        'SELECT id, first_name, last_name, phone_number, email, created_at FROM contacts WHERE id = %s',
        (contact_id,),
        fetchone=True,
    )


def create_contact(data):
    first_name = (data.get('first_name') or '').strip()
    last_name = (data.get('last_name') or '').strip()
    phone_number = (data.get('phone_number') or '').strip()
    email = (data.get('email') or '').strip() or None

    if not first_name or not last_name or not phone_number:
        return {'error': 'first_name, last_name, and phone_number are required.'}

    try:
        return _query(
            'INSERT INTO contacts (first_name, last_name, phone_number, email) VALUES (%s, %s, %s, %s) RETURNING id, first_name, last_name, phone_number, email, created_at',
            (first_name, last_name, phone_number, email),
            fetchone=True,
        )
    except IntegrityError as exc:
        if isinstance(exc.__cause__, errors.UniqueViolation):
            return {'error': 'A contact with that phone number or email already exists.'}
        return {'error': str(exc)}


def update_contact(contact_id, data):
    existing = get_contact_by_id(contact_id)
    if not existing:
        return {'error': 'Contact not found', 'status': 404}

    fields = []
    values = []
    for key in ['first_name', 'last_name', 'phone_number', 'email']:
        if key in data:
            value = (data.get(key) or '').strip()
            if value or key == 'email':
                fields.append(f"{key} = %s")
                values.append(value if value else None)

    if not fields:
        return {'error': 'No update data provided.'}

    values.append(contact_id)
    query = f"UPDATE contacts SET {', '.join(fields)} WHERE id = %s RETURNING id, first_name, last_name, phone_number, email, created_at"
    try:
        result = _query(query, tuple(values), fetchone=True)
        if not result:
            return {'error': 'Contact not found', 'status': 404}
        return result
    except IntegrityError:
        return {'error': 'A contact with that phone number or email already exists.'}
    except Exception as exc:
        return {'error': str(exc)}


def delete_contact(contact_id):
    existing = get_contact_by_id(contact_id)
    if not existing:
        return {'error': 'Contact not found', 'status': 404}

    _query('DELETE FROM contacts WHERE id = %s', (contact_id,))
    return {'status': 'deleted'}
