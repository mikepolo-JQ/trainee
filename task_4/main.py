import pymysql
import conf as settings
import db

command_dict = {
    'create': db.create_tables,
    'drop': db.drop_tables,
    'end': db.connection_close,
    # 'insert': db.insert_data_into_tables
}

try:
    # Connect to the database
    connection = pymysql.connect(host=settings.HOST,
                                 port=settings.PORT,
                                 user=settings.USERNAME,
                                 password=settings.PASSWORD,
                                 database=settings.DATABASE_NAME,
                                 cursorclass=pymysql.cursors.DictCursor)

    print("successfully connected...")

    try:
        with connection.cursor() as cursor:
            # Create a new record

            while True:
                command = input("Write u command...\n")

                result = command_dict[command](connection, cursor)

                if not result:
                    break

    finally:
        connection.close()


except Exception as ex:
    print("Connection refused..")
    print('Exception:\n', ex)
