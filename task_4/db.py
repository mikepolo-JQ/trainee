import json


def create_tables(connection, cursor):
    create_student_table = "CREATE TABLE student(id int primary key," \
                           "name varchar(40)," \
                           "birthday varchar(40)," \
                           "sex varchar(5));"
    cursor.execute(create_student_table)
    connection.commit()

    print("Table student created successfully")

    create_room_table = "CREATE TABLE room(id int primary key," \
                        "name varchar(40));"
    cursor.execute(create_room_table)
    connection.commit()

    print("Table room created successfully")

    create_relationship_table = "CREATE TABLE student_room(id int primary key," \
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


def insert_data_into_tables(connection, cursor):

    with open('students.json') as student_file:
        student_data = json.load(student_file)

    student_inset_values = str()

    for student in student_data:
        student_inset_values += f"({student['id']}, {student['name']}," \
                                f"{student['birthday']}, {student['sex']}), "

    cursor.execute(f"insert into student (id, name, birthday, sex) values {student_inset_values}")
    connection.commit()
    print('Successfully insert into table student')


def connection_close(connection, *args):
    connection.close()
    print('Connection close...')
    return False
