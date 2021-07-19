import json
import time
import pymysql
import conf as settings

sql_queries = {
    'create_student': "create table student(id int primary key," \
                      "name varchar(40)," \
                      "birthday datetime, " \
                      "sex varchar(2));",

    'create_room': "create table room(id int primary key," \
                   "name varchar(40));",

    'create_student_room': "create table student_room(id serial primary key," \
                           "student_id integer references student(id)," \
                           "room_id integer references room(id));",

    'get_room_name_and_count_of_students': "SELECT room.name, COUNT(student_room.student_id) as 'students'" \
                                            " FROM room left JOIN student_room on student_room.room_id=room.id " \
                                            "GROUP BY room.name",

    'get_top5_young_rooms': "SELECT room.name, AVG(YEAR(CURRENT_DATE)-YEAR(student.birthday))" \
                            " AS AverageAge FROM room INNER JOIN student_room " \
                            "on room.id=student_room.room_id INNER JOIN student " \
                            "on student_room.student_id=student.id " \
                            "GROUP BY room.name ORDER BY AverageAge LIMIT 5",

    'biggest_difference_in_the_age': "SELECT room.name, YEAR(MAX(student.birthday))-" \
                                    "YEAR(MIN(student.birthday)) as Difference from room " \
                                    "LEFT JOIN student_room on student_room.room_id=room.id " \
                                    "LEFT JOIN student on student_room.student_id=student.id " \
                                    "GROUP BY room.name ORDER BY Difference DESC LIMIT 5",

    'difference_students_sex': "SELECT room.name FROM room LEFT JOIN student_room " \
                    "ON student_room.room_id=room.id LEFT JOIN student " \
                    "ON student.id=student_room.student_id GROUP BY room.name " \
                    "HAVING MAX(student.sex)!=MIN(student.sex)"
}


class DB:
    def __init__(self):
        # Connect to the database
        connection = pymysql.connect(host=settings.HOST,
                                     port=settings.PORT,
                                     user=settings.USERNAME,
                                     password=settings.PASSWORD,
                                     database=settings.DATABASE_NAME,
                                     cursorclass=pymysql.cursors.DictCursor)

        self.connection = connection
        self.tables_names = ['student', 'room', 'student_room']
        print("Successfully connected...")

    def __disconnect__(self):
        self.connection.close()
        print('Connection close...')

    def __execute_and_commit(self, sql_query: str):
        with self.connection.cursor() as cursor:
            cursor.execute(sql_query)
            self.connection.commit()

    def __fetchall(self, sql_query: str):
        with self.connection.cursor() as cursor:
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            return rows

    # create tables
    def create_table(self) -> bool:
        # if not tables_names:
        tables_names = self.tables_names

        for table_name in tables_names:
            sql_query = sql_queries[f'create_{table_name}']
            self.__execute_and_commit(sql_query)

            print(f"Table {table_name} created successfully")

        return True

    # drop tables
    def drop_table(self) -> bool:

        # if not tables_names:
        tables_names = self.tables_names

        for table_name in tables_names:
            self.__execute_and_commit(f"DROP TABLE {table_name};")
            print(f"Table {table_name} drop successfully")

        return True

    # insert data from student.json to the database
    def insert_from_student_json(self):

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

        self.__execute_and_commit("insert student(id, name, birthday, sex) values " + values + ';')
        print('Insert in student successfully.')

        self.__execute_and_commit("insert student_room(student_id, room_id) values " +
                                  values_for_student_room + ';')

        finish = time.time()
        print(f"Insert in student_room successfully!\nTotal time: {finish - start:.2f}")

    # insert data from room.json to the database
    def insert_from_room_json(self):

        with open('task_4/rooms.json') as room_file:
            room_data = json.load(room_file)

        values = str()

        start = time.time()
        for room in room_data:
            values += f"({room['id']}, '{room['name']}')"

            if room['id'] != room_data[-1]['id']:
                values += ', '

        self.__execute_and_commit("insert room(id, name) values " + values + ';')

        finish = time.time()
        print(f"Insert room successfully! Total time: {finish - start:.2f}")

    def insert_data(self):
        self.insert_from_student_json()
        self.insert_from_room_json()
        return True

    # database queries
    def print_rooms_and_the_number_of_students(self):
        sql_query = sql_queries['get_room_name_and_count_of_students']

        rows = self.__fetchall(sql_query)

        print('\tROOM NAME\tSTUDENTS COUNT')
        for row in rows:
            print(f"\t{row['name']}\t{row['students']}")

        return True

    def print_top5_young_rooms(self):
        sql_query = sql_queries['get_top5_young_rooms']

        rows = self.__fetchall(sql_query)

        print('\tROOM NAME\tAVERAGE AGE')
        for row in rows:
            print(f"\t{row['name']}\t{row['AverageAge']}")

        return True

    def print_top5_rooms_with_the_biggest_difference_in_the_age(self):
        sql_query = sql_queries['biggest_difference_in_the_age']

        rows = self.__fetchall(sql_query)

        print('\tROOM NAME\tDIFFERENCE')
        for row in rows:
            print(f"\t{row['name']}\t{row['Difference']}")

        return True

    def print_rooms_with_difference_students_sex(self):
        sql_query = sql_queries['difference_students_sex']

        rows = self.__fetchall(sql_query)

        print('\tROOM NAME')
        for row in rows:
            print(f"\t{row['name']}")

        return True
