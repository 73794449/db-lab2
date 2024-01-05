from prettytable import from_db_cursor

use_alchemy = True


class View(object):

    @staticmethod
    def show_table_menu(tables):
        num = -1
        while not (list(tables)[0] <= num <= list(tables)[-1]):
            print("Select table:")
            for table in tables:
                print(str(table) + ") " + tables[table][1])

            inp = None
            while inp is None or inp == '':
                inp = input("Input number: ")
            num = int(inp)

        return num

    @staticmethod
    def show_msg(message):
        print(message)

    @staticmethod
    def show_menu():
        num = -1
        while not (num > 0 & num < 7):
            print("\nMenu: ")
            print("1) View table")
            print("2) View all tables")
            print("3) Add to table")
            print("4) Delete from table")
            print("5) Edit table")
            print("6) Exit")
            inp = None
            while inp is None or inp == '':
                inp = input("Input number: ")
            num = int(inp)
        return num

    @staticmethod
    def show_table(table):
        if use_alchemy:
            print(table)
        else:
            print(from_db_cursor(table))

    @staticmethod
    def show_params_menu(params):
        print("\n Input params: ")
        entered_params = {}
        for param in params:
            print(str(param) + ") " + params[param])
            inp = None
            while inp is None or inp == '':
                inp = input("Input value: ")
            entered_params[param] = inp

        return entered_params

    @staticmethod
    def get_id():
        inp = None
        while inp is None or inp == '':
            inp = input("Enter id: ")
        return int(inp)

    @staticmethod
    def show_params_menu_selection(params):
        print("\n Select param: ")
        num = -1
        while not (list(params)[0] <= num <= list(params)[-1]):
            for param in params:
                print(str(param) + ") " + params[param])
            inp = None
            while inp is None or inp == '':
                inp = input("Enter number: ")
            num = int(inp)

        return num

    @staticmethod
    def get_param(param):
        inp = None
        while inp is None or inp == '':
            inp = input("Input value for {}: ".format(param))
        return inp

    @staticmethod
    def show_random_menu():
        inp = None
        while inp is None or inp == '':
            inp = input("Input count of random elements: ")
        return int(inp)

    @staticmethod
    def show_execution_time(time):
        print("Execution time: {}".format(time))

    @staticmethod
    def show_sql_error(error):
        print("Got error from server:\n", error)

    @staticmethod
    def show_sanity_error():
        print("Entered value(s) is(are) not correct")

    @staticmethod
    def show_connection_error():
        print("Connection was not established")
