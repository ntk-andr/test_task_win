import psycopg2

from environs import Env

env = Env()
env.read_env()

conn = psycopg2.connect(
    database=env('POSTGRES_DB'),
    user=env('POSTGRES_USER'),
    password=env('POSTGRES_PASSWORD'),
    host="db",
    port=5432
)

cur = conn.cursor()

cur.execute("SELECT * FROM profile_user_profile")
print(cur.fetchall())


def query(func):

    def wrapper(table_name, **params):
        with conn.cursor() as cursor:
            func(cursor, table_name, **params)
        conn.commit()

    return wrapper


@query
def query_insert(cursor, table_name, **params):
    keyses = values = masks = ''
    for key, value in params.items():
        keyses += f' {key},'
        values += f"'{value}',"
        masks += ' %s,'
    try:
        sql = f'INSERT INTO {table_name} ({keyses[1:-1]}) VALUES ({values[:-1]});'
        cursor.execute(sql, values)
    except Exception as e:
        print(sql)
        print(e)


@query
def query_update_by_id(cursor, table_name, id, **params):
    set_params = ''
    for key, value in params.items():
        set_params += f"{key}='{value}',"
    try:
        sql = f'UPDATE {table_name} SET {set_params[:-1]} WHERE id = {id};'
        cursor.execute(sql)
    except Exception as e:
        print(sql)
        print(e)

# query_insert(table_name='profile_user_profile', name='sdfs', phone=233243)
# query_update_by_id(conn, table_name='profile_user_profile', id=5, name='update!!!')
