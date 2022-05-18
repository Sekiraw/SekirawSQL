import os


def create_database(name):
    if "/" in name or "%" in name:
        print("Can't create database with special characters")
        return 0
    name_string = name
    name = "dbs/" + name
    try:
        os.mkdir(name)
        print("Database " + name_string + " created")
    except FileExistsError:
        print("Database ", + name_string + " already exist")


def delete_database(name):
    name_string = name
    name = "dbs/" + name
    if not os.path.exists(name):
        print("Database " + name_string + " does not exist")
    else:
        try:
            os.rmdir(name)
            print("Database " + name_string + " deleted")
        except FileNotFoundError:
            print("Something went wrong")


