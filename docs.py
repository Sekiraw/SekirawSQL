import os
import constants as cons


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

    return db, doc


def operator_handler(arg):
    arg = arg.split(" ")
    for i in range(len(arg)):
        if "WHERE" in arg[i]:
            return arg[i+1]

    print("Error, operator was not found!")
    return


def create_doc(argument, rules):
    db, doc = get_loc(argument)
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
    if os.path.exists(cons.db_folder + db + "/" + doc + ".ini"):
        os.remove(cons.db_folder + db + "/" + doc + ".ini")
        os.remove(cons.db_folder + db + "/" + doc + "_id.ini")
        os.remove(cons.db_folder + db + "/" + doc + "_rules.ini")
        print("Document " + doc + " deleted successfully")
    else:
        print("The document does not exist")


def add(argument):
    db, doc = get_loc(argument)
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
    print("Rules match! Inserting data.")

    f = open(cons.db_folder + "/" + db + "/" + doc + "_id.ini", "r")
    id = f.read()
    f.close()
    data.insert(0, int(id)+1)

    f = open(cons.db_folder + "/" + db + "/" + doc + "_id.ini", "w")
    f.write(str(int(id)+1))
    f.close()

    f = open(cons.db_folder + "/" + db + "/" + doc + ".ini", "a+")
    f.write(str(data) + ";")
    f.close()


def get(argument):
    db, doc = get_loc(argument)
    op_res = operator_handler(argument)
    op_res = op_res.split("?")
    field = op_res[0]
    operator = op_res[1]
    value = op_res[2]

    f = open(cons.db_folder + "/" + db + "/" + doc + ".ini", "r")
    data = f.read().split(";")
    f.close()
    print(op_res)
    f = open(cons.db_folder + "/" + db + "/" + doc + "_rules.ini", "r")
    rules = f.read()
    f.close()
    rules = rules.split(", ")
    aoi = 0
    for i in range(len(rules)):
        if str(field) in str(rules[i]):
            aoi = i

    print(aoi)

    # num_str = ""
    #
    # if operator == "==":
    #     num_str += data[aoi][1]
    #     if data[aoi][2].isnumeric():
    #         num_str += data[aoi][2]
    #
    #     print(num_str)
    #
    # for i in range(len(data)):
    #     print(list(data[i][2]))
    #     if data[i] == int(value):
    #         print("a")
