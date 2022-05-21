import os
from collections import Counter
from pathlib import Path

import constants as cons


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


def create_doc(argument, rules):
    db, doc = get_loc(argument)
    if check_argument_rules(argument):
        return

    try:
        f = open(cons.db_folder + db + "/" + doc + ".ini", "w")
        f.write("")
        f.close()
        print("Document " + doc + " created successfully")
        f = open(cons.db_folder + "/" + db + "/" + doc + "_id.ini", "w")
        f.write(str(0))
        f.close()
        create_doc_rules(db, doc, rules)
    except FileExistsError:
        print("Document " + doc + " already exists")


def create_doc_rules(db, doc, rules):
    f = open(cons.db_folder + db + "/" + doc + "_rules" + ".ini", "w")
    f.write(rules)
    f.close()


def delete_doc(argument):
    db, doc = get_loc(argument)
    if check_argument_rules(argument):
        return

    if os.path.exists(cons.db_folder + db + "/" + doc + ".ini"):
        os.remove(cons.db_folder + db + "/" + doc + ".ini")
        os.remove(cons.db_folder + db + "/" + doc + "_id.ini")
        os.remove(cons.db_folder + db + "/" + doc + "_rules.ini")
        print("Document " + doc + " deleted successfully")
    else:
        print("The document does not exist")


def add(argument, test_run=False):
    db, doc = get_loc(argument)
    if check_argument_rules(argument):
        return
    arg = argument.split(" ")
    # check the rules first
    f = open(cons.db_folder + "/" + db + "/" + doc + "_rules.ini", "r")
    rules = f.read()
    f.close()
    rules = rules.replace(" ", "")
    rules = rules.split(",")
    rules.pop(0)

    data = arg[0].split(",")

    for i in range(len(rules)):
        if "int" in rules[i]:
            if not data[i].isnumeric():
                print("Inserted value doesn't match the rules")
                return
            if len(data) != len(rules):
                print("Given values doesn't match the rules")
                print("Rules: ", rules)
                return
    print("Rules match! Inserting data.")

    f = open(cons.db_folder + "/" + db + "/" + doc + "_id.ini", "r")
    id = f.read()
    f.close()
    data.insert(0, int(id)+1)
    data = str(data).replace("'", "")
    print(data)

    if not test_run:
        f = open(cons.db_folder + "/" + db + "/" + doc + "_id.ini", "w")
        f.write(str(int(id)+1))
        f.close()

        f = open(cons.db_folder + "/" + db + "/" + doc + ".ini", "a+")
        f.write(str(data) + ";")
        f.close()
    else:
        print("No errors were found.")
        print("Test was successful!")


def get(argument):
    db, doc = get_loc(argument)
    if check_argument_rules(argument):
        return

    op_res, second = operator_reader(argument)
    op_res = op_res.split("?")
    field = op_res[0]
    operator = op_res[1]
    value = op_res[2]

    f = open(cons.db_folder + "/" + db + "/" + doc + ".ini", "r")
    data = f.read().split(';')
    f.close()
    # print(op_res)
    f = open(cons.db_folder + "/" + db + "/" + doc + "_rules.ini", "r")
    rules = f.read()
    f.close()
    rules = rules.split(", ")
    aoi = -1
    for i in range(len(rules)):
        if str(field) in str(rules[i]):
            aoi = i

    if aoi == -1:
        print("Field " + str(field) + " was not found in rules!")
        return

    # print(aoi)
    ls = []
    # convert the string lists into lists
    for i in range(len(data)):
        ls.append(data[i].strip('][').split(', '))

    # print(ls)
    # print(len(ls))

    res = operator_handler(operator, ls, aoi, value)

    # second query if there is an AND in the argument
    if second != "":
        second_get = get("INDB " + db + " FROM " + doc + " WHERE " + second)
        merged = res + second_get
        merged.sort()
        # method for keeping only the multiples
        n_res = []
        aux = 0
        aux2 = 0
        for i in merged:
            aux2 = i
            if (aux2 == aux):
                n_res.append(i)
            aux = i
        return n_res
    else:
        return res


def update(argument, test_run=False):
    db, doc = get_loc(argument)
    if check_argument_rules(argument):
        return

    op_res, second = operator_reader(argument)
    op_res = op_res.split("?")
    up_to, field_up_to = update_to(argument)
    field = op_res[0]
    operator = op_res[1]
    value = op_res[2]

    f = open(cons.db_folder + "/" + db + "/" + doc + ".ini", "r")
    data = f.read().split(';')
    f.close()
    # print(op_res)
    f = open(cons.db_folder + "/" + db + "/" + doc + "_rules.ini", "r")
    rules = f.read()
    f.close()
    rules = rules.split(", ")
    aoi = -1
    a_to_up = -1
    for i in range(len(rules)):
        if str(field) in str(rules[i]):
            aoi = i

    if aoi == -1:
        print("Field " + str(field) + " was not found in rules!")
        return

    for i in range(len(rules)):
        if str(field_up_to) in str(rules[i]):
            a_to_up = i

    if a_to_up == -1:
        print("Field was not found in rules!")
        return

    # print(aoi)
    # print(a_to_up)
    ls = []
    # convert the string lists into lists
    for i in range(len(data)):
        ls.append(data[i].strip('][').split(', '))

    # print(ls)
    # print(len(ls))

    if operator == "==":
        for i in range(len(ls) - 1):
            if str(ls[i][aoi]) == str(value):
                ls[i][a_to_up] = up_to

    # convert list to the unique string that the db uses
    data_back = datafy_list(ls)
    # print(data_back)
    if not test_run:
        f = open(cons.db_folder + "/" + db + "/" + doc + ".ini", "w")
        f.write(data_back)
        f.close()
        print("Updated successfully!")
    else:
        print("No errors were found.")
        print("Test was successful!")
    # print(data_back)


def delete(argument, test_run=False):
    db, doc = get_loc(argument)
    if check_argument_rules(argument):
        return

    op_res, second = operator_reader(argument)
    op_res = op_res.split("?")
    field = op_res[0]
    operator = op_res[1]
    value = op_res[2]

    f = open(cons.db_folder + "/" + db + "/" + doc + ".ini", "r")
    data = f.read().split(';')
    f.close()
    # print(op_res)
    f = open(cons.db_folder + "/" + db + "/" + doc + "_rules.ini", "r")
    rules = f.read()
    f.close()
    rules = rules.split(", ")
    aoi = -1
    for i in range(len(rules)):
        if str(field) in str(rules[i]):
            aoi = i

    if aoi == -1:
        print("Field " + str(field) + " was not found in rules!")
        return

    # print(aoi)
    # print(a_to_up)
    ls = []
    # convert the string lists into lists
    for i in range(len(data)):
        ls.append(data[i].strip('][').split(', '))

    # print(ls)
    # print(len(ls))

    values_to_delete = operator_handler(operator, ls, aoi, value)

    # skip the elements that are the same
    res = []

    for i in range(len(ls)):
        if ls[i] not in values_to_delete:
            res.append(ls[i])

    res = datafy_list(res)

    if not test_run:
        f = open(cons.db_folder + "/" + db + "/" + doc + ".ini", "w")
        f.write(res)
        f.close()
        print("Deleted successfully!")
    else:
        print("No errors were found.")
        print("Test was successful!")
    # print(data_back)


def get_rules(argument):
    db, doc = get_loc(argument)
    f = open(cons.db_folder + "/" + db + "/" + doc + ".ini", "r")
    print(f.read())
    f.close()


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


# convert the list to the unique system that the database uses
def datafy_list(list):
    string = str(list).replace("'", "")
    string = str(string).replace("[]", "")
    string = str(string).replace("],", "];")
    string = str(string).replace("; ", ";")
    string = string[1:]
    string = string[:-1]
    return string


def check_argument_rules(argument):
    for i in range(len(argument)):
        if argument[i] in cons.banned_characters:
            print("Banned character found")
            return True

    return False
