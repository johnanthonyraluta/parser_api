import mysql.connector as MySQL

def sql_connection():
    db = MySQL.connect(
        host="10.66.69.144",
        user="jmawirat",
        password="cisco",
        #port=1099,
        database='service_discovery_nso_db'
        )

    #cur = db.cursor()
    return db


