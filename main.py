from controller import Controller

connection_settings = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 't3',
    'host': 'localhost',
    'port': 5432
}

if __name__ == '__main__':  # Startup controller
    controller = Controller(connection_settings)
    controller.run()
