import sqlite3


db = sqlite3.connect('project.db')
cur = db.cursor()

def create_db():
    try:
        cur.execute('''CREATE TABLE banks
                (name text type UNIQUE, bank_id integer, active bool)''')
    except:
        pass

create_db()


def create_db_sites():
    try:
        cur.execute('''CREATE TABLE sites
                (bank_name text type UNIQUE, site_link text)''')
    except:
        pass


create_db_sites()

def create_db__fake_sites():
    try:
        cur.execute('''CREATE TABLE fakesites
                (bank_name text type UNIQUE, site_link text type UNIQUE)''')
    except:
        pass


create_db__fake_sites()


def add_bank(name:str, bank_id:int, active:bool):
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO banks VALUES (?, ?, ?)", (name, bank_id, active))
        db.commit()
    except:
        pass


def add_site(bank_name:str, site_link:str):
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO sites VALUES (?, ?)", (bank_name, site_link))
        db.commit()
    except:
        pass


def add_fake_site(bank_name:str, site_link:str):
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO fakesites VALUES (?, ?)", (bank_name, site_link))
        db.commit()
    except:
        pass


def select_banks_data():
    cur = db.cursor()
    cur.execute("SELECT * FROM banks")
    rows = cur.fetchall()
    return rows


def select_official_site_data():
    cur = db.cursor()
    cur.execute("SELECT * FROM sites")
    rows = cur.fetchall()
    return rows


def select_fake_site_data():
    cur = db.cursor()
    cur.execute("SELECT * FROM fakesites")
    rows = cur.fetchall()
    return rows


def close_db():
    db.close()



# CRUD - create, read, update, delete