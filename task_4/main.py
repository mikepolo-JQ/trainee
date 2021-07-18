import pymysql
import conf as settings
import db

command_dict = {
    'create': db.create_tables,
    'drop': db.drop_tables,
    'end': db.connection_close,
    'insert': db.insert_data_into_tables,

    '1': db.get_rooms_and_the_number_of_students
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

            print("""
                Hello! U can use one of this command:
                    create
                    drop
                    insert 
                    end
            """)

            while True:

                command = input("Write u command...\n")

                try:
                    result = command_dict[command]
                except KeyError as ex:
                    print("First! Bed request!")
                    continue

                if not result:
                    break

                result(connection, cursor)

    finally:
        connection.close()


except Exception as ex:
    print("Connection refused..")
    print('Exception:\n', ex)
