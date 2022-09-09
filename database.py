import os
from constants import db_folder


def create_database(name):
    if "/" in name or "%" in name:
        print("Can't create database with special characters")
        return 0
    name_string = name
    name = db_folder.join(name)
    try:
        os.mkdir(name)
        print(''.join(["Database ", name_string, ' created successfully']))
    except FileExistsError:
        print(''.join(["Database ", name_string, ' already exists']))


def delete_database(name):
    name_string = name
    name = db_folder.join(name)
    if not os.path.exists(name):
        print(''.join(["Database ", name_string, " doesn't exists"]))
    else:
        try:
            os.rmdir(name)
            print(''.join(["Database ", name_string, ' deleted successfully']))
        except FileNotFoundError:
            print("Something went wrong")


