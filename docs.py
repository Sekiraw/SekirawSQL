import os

import constants as cons
import private_func as pf


def create_doc(argument, rules):
    db, doc = pf.get_loc(argument)
    if pf.check_argument_rules(argument):
        return cons.banned_error

    try:
        f = open(cons.db_folder + db + "/" + doc + ".ini", "w")
        f.write("")
        f.close()
        print("Document " + doc + " created successfully")
        f = open(cons.db_folder + "/" + db + "/" + doc + "_id.ini", "w")
        f.write(str(0))
        f.close()
        pf.create_doc_rules(db, doc, rules)
    except FileExistsError:
        print("Document " + doc + " already exists")


def delete_doc(argument):
    db, doc = pf.get_loc(argument)
    if pf.check_argument_rules(argument):
        return cons.banned_error

    if os.path.exists(cons.db_folder + db + "/" + doc + ".ini"):
        os.remove(cons.db_folder + db + "/" + doc + ".ini")
        os.remove(cons.db_folder + db + "/" + doc + "_id.ini")
        os.remove(cons.db_folder + db + "/" + doc + "_rules.ini")
        print("Document " + doc + " deleted successfully")
    else:
        print("The document does not exist")


def add(argument, test_run=False):
    db, doc = pf.get_loc(argument)
    if pf.check_argument_rules(argument):
        return cons.banned_error
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
                return "Inserted value doesn't match the rules"
            if len(data) != len(rules):
                print("Given values doesn't match the rules" + "\nRules: " + str(rules))
                return "Given values doesn't match the rules" + "\nRules: " + str(rules)
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
        print("No errors were found. Test was successful!")
        return "No errors were found. Test was successful!"


def get(argument):
    db, doc = pf.get_loc(argument)
    if pf.check_argument_rules(argument):
        return cons.banned_error
    order = ""
    op_res, second = pf.operator_reader(argument)
    order, is_desc = pf.sort_operator_reader(argument)
    op_res = op_res.split("?")
    field = op_res[0]
    operator = op_res[1]
    value = op_res[2]

    # open and read the doc
    f = open(cons.db_folder + "/" + db + "/" + doc + ".ini", "r")
    data = f.read().split(';')
    f.close()
    # print(op_res)
    # open and read the rules
    f = open(cons.db_folder + "/" + db + "/" + doc + "_rules.ini", "r")
    rules = f.read()
    f.close()
    rules = rules.split(", ")
    aoi = -1
    aoi_order = -1 if order != "" else -2
    for i in range(len(rules)):
        if str(field) in str(rules[i]):
            aoi = i
        if order != "":
            if str(order) in str(rules[i]):
                aoi_order = i

    # if aoi kept -1, that means there was no field in the rules that was given
    if aoi == -1:
        return "Field '" + str(field) + "' was not found in rules!"
    elif aoi_order == -1:
        return "Field '" + str(order) + "' was not found in rules!"

    # print(aoi)
    ls = []
    # convert the string lists into lists
    for i in range(len(data)):
        ls.append(data[i].strip('][').split(', '))

    # print(ls)
    # print(len(ls))

    res = pf.operator_handler(operator, ls, aoi, value)

    # second query if there is an AND in the argument
    if second != "":
        n_res = pf.and_arg(db, doc, order, second, is_desc, res, get)

        if order != "":
            l = []
            res = pf.unique_sorter(n_res, aoi_order, l, is_desc if is_desc else False)
            return res
        return n_res
    else:
        # if ORDER BY was found in the argument
        if order != "":
            l = []
            res = pf.unique_sorter(res, aoi_order, l, is_desc if is_desc else False)
        return res


def update(argument, test_run=False):
    db, doc = pf.get_loc(argument)
    if pf.check_argument_rules(argument):
        return cons.banned_error

    op_res, second = pf.operator_reader(argument)
    op_res = op_res.split("?")
    up_to, field_up_to = pf.update_to(argument)
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
        return "Field '" + str(field) + "' was not found in rules!"

    for i in range(len(rules)):
        if str(field_up_to) in str(rules[i]):
            a_to_up = i

    if a_to_up == -1:
        return "Field '" + str(field_up_to) + "' was not found in rules!"

    # print(aoi)
    # print(a_to_up)
    ls = []
    # convert the string lists into lists
    for i in range(len(data)):
        ls.append(data[i].strip('][').split(', '))

    # print(ls)
    # print(len(ls))

    # have to update for more operators
    # if operator == "==":
    #     for i in range(len(ls) - 1):
    #         if str(ls[i][aoi]) == str(value):
    #             ls[i][a_to_up] = up_to
    ls = pf.update_operator_handler(operator, ls, aoi, value, a_to_up, up_to)

    # convert list to the unique string that the db uses
    data_back = pf.datafy_list(ls)
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
    db, doc = pf.get_loc(argument)
    if pf.check_argument_rules(argument):
        return cons.banned_error

    op_res, second = pf.operator_reader(argument)
    op_res = op_res.split("?")
    field = op_res[0]
    operator = op_res[1]
    value = op_res[2]
    if field == "" or operator == "" or value == "":
        print("Operator not found.")
        return

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
        return "Field '" + str(field) + "' was not found in rules!"

    # print(aoi)
    # print(a_to_up)
    ls = []
    # convert the string lists into lists
    for i in range(len(data)):
        ls.append(data[i].strip('][').split(', '))

    # print(ls)
    # print(len(ls))

    values_to_delete = pf.operator_handler(operator, ls, aoi, value)
    print(values_to_delete)
    # skip the elements that are the same
    res = []

    for i in range(len(ls)):
        if ls[i] not in values_to_delete:
            res.append(ls[i])

    # print(res)
    # if second != "":
    #     n_res = pf.and_arg_no_order(db, doc, second, res, delete)
    #     print(n_res)

    res = pf.datafy_list(res)

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
    db, doc = pf.get_loc(argument)
    f = open(cons.db_folder + "/" + db + "/" + doc + ".ini", "r")
    print(f.read())
    f.close()
