import json
import time


def create_tables(connection, cursor):
    create_student_table = "create table student(id int primary key," \
                           "name varchar(40)," \
                           "birthday varchar(40)," \
                           "sex varchar(5));"
    cursor.execute(create_student_table)
    connection.commit()

    print("Table student created successfully")

    create_room_table = "create table room(id int primary key," \
                        "name varchar(40));"
    cursor.execute(create_room_table)
    connection.commit()

    print("Table room created successfully")

    create_relationship_table = "create table student_room(id serial primary key," \
                                "student_id integer references student(id)," \
                                "room_id integer references room(id));"
    cursor.execute(create_relationship_table)
    connection.commit()

    print("Table student_room created successfully")

    return True


def drop_tables(connection, cursor):

    cursor.execute("DROP TABLE student;")
    connection.commit()
    print("Table student drop successfully")

    cursor.execute("DROP TABLE room;")
    connection.commit()

    print("Table room created successfully")

    cursor.execute("DROP TABLE student_room;")
    connection.commit()
    print("Table student_room drop successfully")
    return True


def insert_into_student_table(connection, cursor):

    with open('task_4/students.json') as student_file:
        student_data = json.load(student_file)

    values = str()
    values_for_student_room = str()

    start = time.time()
    for student in student_data:
        values += f"({student['id']}, '{student['name']}', '{student['birthday']}', '{student['sex']}')"

        values_for_student_room += f"({student['id']}, {student['room']})"

        if student['id'] != student_data[-1]['id']:
            values += ', '
            values_for_student_room += ', '

    cursor.execute("insert student(id, name, birthday, sex) values " + values + ';')
    connection.commit()

    cursor.execute("insert student_room(student_id, room_id) values " +
                   values_for_student_room + ';')
    connection.commit()
    finish = time.time()
    print(f"Insert student and student_room successfully! Total time: {finish - start:.2f}")
    return True


def insert_into_room_table(connection, cursor):

    with open('task_4/rooms.json') as room_file:
        room_data = json.load(room_file)

    values = str()

    start = time.time()
    for room in room_data:
        values += f"({room['id']}, '{room['name']}')"

        if room['id'] != room_data[-1]['id']:
            values += ', '

    cursor.execute("insert room(id, name) values " + values + ';')
    connection.commit()

    finish = time.time()

    print(f"Insert room successfully! Total time: {finish - start:.2f}")

    return True


def insert_data_into_tables(connection, cursor):
    insert_into_student_table(connection, cursor)
    insert_into_room_table(connection, cursor)


# database queries
def get_rooms_and_the_number_of_students(connection, cursor):
    sql_query = "SELECT room.name, COUNT(student_room.student_id) as 'students'" \
                " FROM room left JOIN student_room on student_room.room_id=room.id " \
                "GROUP BY room.name ORDER BY room.id"

    cursor.execute(sql_query)

    result = cursor.fetchall()

    print(result)

    return True


def connection_close(connection, *args):
    connection.close()
    print('Connection close...')
    return False
