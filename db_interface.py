import sqlite3

TABLE_ANONS = "anons"  # T_ as in TABLE

class DatabaseInterface:
    _instance = None

    @staticmethod
    def Get():
        if not DatabaseInterface._instance:
            DatabaseInterface._instance = DatabaseInterface()
        return DatabaseInterface._instance

    def setup(self):
        connection = None
        try:
            connection = sqlite3.connect(self._name)
            cursor = connection.cursor()

            # check if the table anons was created
            if not cursor.execute(f"SELECT name from sqlite_master WHERE name='{TABLE_ANONS}'").fetchone():
                query = f"CREATE TABLE {TABLE_ANONS} (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER UNI1UE, alias TEXT NOT NULL)"

                # create table anon
                cursor.execute(query)

                print(f"{TABLE_ANONS} table created successfuly.")

            print("Database setup completed.")    
            connection.close()
        except Exception as ex:
            if connection:
                connection.close()
            raise ex  # create custom exception for this


    def add_anon(self, anon):
        connection = None
        if not anon:
            raise Exception("You must provide an Anon onnect to save")
        try:
            query = f"INSERT INTO {TABLE_ANONS} (user_id, alias) VALUES (?, ?)"
            connection = sqlite3.connect(self._name)
            cursor = connection.cursor()
            cursor.execute(query, (anon.user_id, anon.alias))
            connection.close()
        except Exception as ex:
            if connection:
                connection.close()
            raise ex  # custom ex needed here too

    def get_user(self, user_id):
        connection = sqlite3.connect(self._name)
        cursor = connection.cursor()
        res = connection.execute(f"SELECT * FROM {TABLE_ANONS} WHERE user_id={user_id}")
        # whatever next
        
    def __init__(self, name="data.db"):
        self._name = name
        self.setup()
        #res = cursor.execute("SELECT * FROM " + TABLE_ANONS)
        #print(res)