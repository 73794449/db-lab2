from sqlalchemy.exc import SQLAlchemyError

from model import Model
from view import View


class Controller:
    def __init__(self, connection_settings):  # Startup for model and view
        self.view = View()
        try:
            self.model = Model(connection_settings)
        except SQLAlchemyError:
            self.view.show_connection_error()
            exit(-1)

    def run(self):  # Menu
        menu = {
            1: self.view_table,
            2: self.view_all_tables,
            3: self.add_table,
            4: self.delete_table,
            5: self.edit_table,
        }
        while True:
            choice = self.view.show_menu()
            if choice == 6:
                break
            elif choice in menu:
                menu[choice]()

    def view_table(self):
        try:
            selected = self.view.show_table_menu(self.model.tables)
            table = self.model.get_table(selected)
            self.view.show_table(table)
        except SQLAlchemyError as error:
            self.view.show_sql_error(str(error.__dict__['orig']))

    def view_all_tables(self):
        try:
            for i in self.model.tables:
                table = self.model.get_table(i)
                self.view.show_msg(self.model.tables[i])
                self.view.show_table(table)
        except SQLAlchemyError as error:
            self.view.show_sql_error(str(error.__dict__['orig']))

    def add_table(self):
        try:
            selected = self.view.show_table_menu(self.model.tables)
            table = self.model.get_table(selected)
            self.view.show_table(table)
            needed_params = self.model.get_params(selected)
            entered_params = self.view.show_params_menu(needed_params)
            self.model.add_table(selected, entered_params)
        except SQLAlchemyError as error:
            self.view.show_sql_error(str(error.__dict__['orig']))

    def delete_table(self):
        try:
            selected = self.view.show_table_menu(self.model.tables)
            table = self.model.get_table(selected)
            self.view.show_table(table)
            self.view.show_msg("Select id to delete: ")
            id_to_delete = self.view.get_id()
            status = self.model.delete_table(selected, id_to_delete)
            if not status:
                self.view.show_sql_error("Deleting error")
        except SQLAlchemyError as error:
            self.view.show_sql_error(str(error.__dict__['orig']))

    def edit_table(self):
        try:
            selected = self.view.show_table_menu(self.model.tables)
            table = self.model.get_table(selected)
            self.view.show_table(table)
            self.view.show_msg("Select id to edit: ")
            id_to_edit = self.view.get_id()
            available_params = self.model.get_params(selected)
            selected_param = self.view.show_params_menu_selection(available_params)
            selected_param_value = self.view.get_param(available_params[selected_param])
            self.model.edit_table(selected, id_to_edit, selected_param, selected_param_value)
        except SQLAlchemyError as error:
            self.view.show_sql_error(str(error.__dict__['orig']))
