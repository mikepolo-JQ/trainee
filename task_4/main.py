import pymysql
import conf as settings
import db

command_dict = {
    'create': db.create_tables,
    'drop': db.drop_tables,
    'end': db.connection_close,
    'insert': db.insert_data_into_tables,
    'clear': db.clear,
    '?': db.print_command_list,

    '1': db.get_rooms_and_the_number_of_students,
    '2': db.get_top5_young_rooms,
    '3': db.get_top5_biggest_difference_in_the_age_rooms,
    '4': db.get_rooms_with_difference_students_sex
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

                command = input("TASK_4 >>> ").lower()

                try:
                    handler = command_dict[command]
                except KeyError as ex:
                    print("Bed request! Try '?' for see command list.")
                    continue

                result = handler(connection, cursor)

                if not result:
                    break

    finally:
        connection.close()


except Exception as ex:
    print("Connection refused..")
    print('Exception:\n', ex)
