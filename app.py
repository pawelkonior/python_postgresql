from psycopg2 import connect, OperationalError, sql, DatabaseError

try:
    cnx = connect(user='postgres',
                  password='password',
                  host='localhost',
                  port=5432,
                  database='postgres')
    cursor = cnx.cursor()

except OperationalError as err:
    print('Connection error')
    raise ValueError(f'Connection error: {err}')

query_create_tb = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {table_name}(
    id SERIAL,
    name VARCHAR(50),
    email VARCHAR(120) UNIQUE,
    password VARCHAR(60) DEFAULT 'ala',
    PRIMARY KEY (id))
""").format(table_name=sql.Identifier('User'))

query_create_tb_address = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {table_name}(
    id SERIAL,
    user_id SMALLINT,
    street VARCHAR(150),
    city VARCHAR(100),
    notes TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES {table_name_foreign}(id))
""").format(
    table_name=sql.Identifier('Address'),
    table_name_foreign=sql.Identifier('User')
)

query_insert = sql.SQL("""INSERT INTO {table_name}(name, email, password)
VALUES (%s, %s, %s)""").format(table_name=sql.Identifier('User'))

query_delete = sql.SQL("""DELETE FROM {table_name} WHERE id=%s""").format(
    table_name=sql.Identifier('User')
)

query_update = sql.SQL("""UPDATE {table_name} SET email=%s  WHERE id=%s""").format(
    table_name=sql.Identifier('User')
)

query_alter = sql.SQL("""ALTER TABLE {table_name} ADD COLUMN price DECIMAL(7,2) DEFAULT 0""").format(
    table_name=sql.Identifier('User'))

query_alter2 = sql.SQL(
    """ALTER TABLE {table_name} ADD COLUMN date_of_created TIMESTAMP DEFAULT
     CURRENT_TIMESTAMP""").format(
    table_name=sql.Identifier('Address'))

try:
    with cnx, cnx.cursor() as cs:
        try:
            cs.execute(query_create_tb_address)
        except DatabaseError as err:
            print(err)

        try:
            cs.execute(query_insert, ('ala', 'a@a.pl', 'secret'))
        except DatabaseError as err:
            print(err)

        # try:
        #     cs.execute(query_delete, (1,))
        # except DatabaseError as err:
        #     print(err)

        # try:
        #     cs.execute(query_update, ('b@b.pl', 3))
        # except DatabaseError as err:
        #     print(err)

        # try:
        #     cs.execute(query_alter)
        # except DatabaseError as err:
        #     print(err)

        try:
            cs.execute(query_alter2)
        except DatabaseError as err:
            print(err)
finally:
    cnx.close()
