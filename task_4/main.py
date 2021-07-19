from db import DB


help_string = """
List of all TASK_4 commands:
?\t\tGet list of commands
create\t\tCreate tables student, rooms and student_room for m2m rel
drop\t\tDrop all tables
insert\t\tEnter data from json file to the database
end\t\tExit from TASK_4
clear\t\tClear the terminal\n
1\t\tGet list of rooms and the number of students in each of them
2\t\tGet top 5 rooms with the smallest average age of students
3\t\tGet top 5 rooms with the biggest difference in the age of students
4\t\tGet list of rooms where students of different sexes live
"""


def print_command_list(_x):
    print(help_string)
    return True


def clear(_x):
    import os
    os.system('clear||cls')
    return True


command_dict = {
    'create': DB.create_table,
    'drop': DB.drop_table,
    'end': lambda _x: False,
    'insert': DB.insert_data,
    'clear': clear,
    '?': print_command_list,

    '1': DB.print_rooms_and_the_number_of_students,
    '2': DB.print_top5_young_rooms,
    '3': DB.print_top5_rooms_with_the_biggest_difference_in_the_age,
    '4': DB.print_rooms_with_difference_students_sex
}


try:
    # Connect to the database
    db_helper = DB()

    try:
        while True:

            command = input("TASK_4 >>> ").lower()

            try:
                handler = command_dict[command]
            except KeyError as ex:
                print("Bed request! Try '?' for see command list.")
                continue

            result = handler(db_helper)

            if not result:
                break

    finally:
        db_helper.__disconnect__()


except Exception as ex:
    print("Connection refused..")
    print('Exception:\n', ex)
