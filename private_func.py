import constants as cons
from pathlib import Path


def create_doc_rules(db, doc, rules):
    f = open(cons.db_folder + db + "/" + doc + "_rules" + ".ini", "w")
    f.write(rules)
    f.close()


def update_to(arg):
    arg = arg.split(" ")
    up_to = ""
    field_up_to = ""
    for i in range(len(arg)):
        if arg[i] == "TO":
            up_to = arg[i+1]
        if arg[i] == "UPDATE":
            field_up_to = arg[i+1]

    return up_to, field_up_to


# convert the list to the unique system that the database uses
def datafy_list(list):
    string = str(list).replace("'", "")
    string = str(string).replace("[]", "")
    string = str(string).replace("],", "];")
    string = str(string).replace("; ", ";")
    string = string[1:]
    string = string[:-1]
    return string


# finds and returns the location of the given database and document
def get_loc(arg):
    db = ""
    doc = ""
    arg = arg.split(' ')
    for i in range(len(arg)):
        if "INDB" in arg[i]:
            db = str(arg[i + 1])
        if "INTO" in arg[i]:
            doc = str(arg[i + 1])
        if "CRDOC" in arg[i]:
            doc = str(arg[i + 1])
        if "DLDOC" in arg[i]:
            doc = str(arg[i + 1])
        if "FROM" in arg[i]:
            doc = str(arg[i + 1])
    if doc == "" or db == "":
        print("Something went wrong")
        return

    # check if file exists
    location = Path(cons.db_folder + "/" + db + "/" + doc + ".ini")
    if location.exists():
        return db, doc
    else:
        print("Cannot find document.")
        return db, doc


def operator_reader(arg):
    arg = arg.split(" ")
    where = ""
    andd = ""
    for i in range(len(arg)):
        if "WHERE" in arg[i]:
            where = arg[i+1]
        if "AND" in arg[i]:
            andd = arg[i+1]

    if where == "":
        print("Error, operator was not found!")
        return
    else:
        return where, andd


def operator_handler(operator, list, aoi, value):
    res = []
    if operator == "==":
        for i in range(len(list) - 1):
            if str(list[i][aoi]) == str(value):
                res.append(list[i])
    elif operator == "!=":
        for i in range(len(list)-1):
            if str(list[i][aoi]) != str(value):
                res.append(list[i])
    elif operator == ">":
        for i in range(len(list)-1):
            if list[i][aoi] > str(value):
                res.append(list[i])
    elif operator == "<":
        for i in range(len(list)-1):
            if list[i][aoi] < str(value):
                res.append(list[i])
    elif operator == ">=":
        for i in range(len(list)-1):
            if list[i][aoi] >= str(value):
                res.append(list[i])
    elif operator == "<=":
        for i in range(len(list)-1):
            if list[i][aoi] <= str(value):
                res.append(list[i])

    return res


def check_argument_rules(argument):
    for i in range(len(argument)):
        if argument[i] in cons.banned_characters:
            print("Banned character found")
            return True

    return False