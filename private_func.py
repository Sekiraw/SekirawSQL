import constants as cons
from pathlib import Path


def update_to(argument):
    up_to, field_up_to = '', ''
    for i in range(len(argument)):
        if argument[i] == "TO":
            up_to = argument[i+1]
        if argument[i] == "UPDATE":
            field_up_to = argument[i+1]

    return up_to, field_up_to


# convert the list to the unique system that the database uses
def datafy_list(input_list):
    string = str(input_list).replace("'", "")
    string = str(string).replace("[]", "")
    string = str(string).replace("],", "];")
    string = str(string).replace("; ", ";")
    string = string[1:]
    string = string[:-1]
    string = string + ';'
    return string


# finds and returns the location of the given database and document
def get_loc(arg, db):
    doc = ""
    for i in range(len(arg)):
        if "INTO" in arg[i]:
            doc = str(arg[i + 1])
        elif "CRDOC" in arg[i]:
            doc = str(arg[i + 1])
        elif "DLDOC" in arg[i]:
            doc = str(arg[i + 1])
        elif "FROM" in arg[i]:
            doc = str(arg[i + 1])
    if doc == "":
        print("Something went wrong, argument is not valid")
        return

    # check if file exists
    location = Path(''.join([cons.db_folder, db, '/', doc, cons.file_extension]))
    if location.exists():
        return doc
    else:
        print("Cannot find document.")
        return doc


def limit(argument):
    # don't split it if it's not even in there
    limit_count = 0
    for i in range(len(argument)):
        if argument[i] == "LIMIT":
            limit_count = argument[i+1]
    return limit_count


def operator_reader(arg):
    where, only, select_all = '', '', False
    andd = []
    for i in range(len(arg)):
        if "WHERE" in arg[i]:
            where = arg[i+1]
        if "AND" in arg[i]:
            andd.append(arg[i+1])
        if "ONLY" in arg[i]:
            only = arg[i+1]
        if "SELECTALL" in arg[i]:
            select_all = True

    if where == "" and not select_all:
        print("Error, operator was not found!")
        return
    else:
        return where, andd, only, select_all



def sort_operator_reader(argument):
    parameter = ""
    desc = False
    for i in range(len(argument)):
        if argument[i] == "ORDER" and argument[i+1] == "BY":
            parameter = argument[i+2]
        if argument[i] == "DESC":
            desc = True

    return parameter, desc


def unique_sorter(ls, aoi, rev):
    return sorted(ls, key=lambda x: x[aoi], reverse=rev)


# keep it for maybe later uses
def and_arg_no_order(doc, second, res, delete):
    second_delete = delete(''.join(["FROM ", doc, " WHERE ", second]))
    merged = res + second_delete
    merged.sort()
    # method for keeping only the multiples
    n_res = []
    aux, aux2 = 0, 0
    for i in merged:
        aux2 = i
        if aux2 == aux:
            n_res.append(i)
        aux = i

    return n_res


def operator_handler(operator, i_list, aoi, value):
    res = []
    num = value.isnumeric()
    if operator == "==":
        for i in range(len(i_list)):
            if (str(i_list[i][aoi]) if not num else int(i_list[i][aoi])) == (str(value) if not num else int(value)):
                res.append(i_list[i])
    elif operator == "!=":
        for i in range(len(i_list)):
            if (str(i_list[i][aoi]) if not num else int(i_list[i][aoi])) != (str(value) if not num else int(value)):
                res.append(i_list[i])
    elif operator == ">":
        for i in range(len(i_list)):
            if (str(i_list[i][aoi]) if not num else int(i_list[i][aoi])) > (str(value) if not num else int(value)):
                res.append(i_list[i])
    elif operator == "<":
        for i in range(len(i_list)):
            if (str(i_list[i][aoi]) if not num else int(i_list[i][aoi])) < (str(value) if not num else int(value)):
                res.append(i_list[i])
    elif operator == ">=":
        for i in range(len(i_list)):
            if (str(i_list[i][aoi]) if not num else int(i_list[i][aoi])) >= (str(value) if not num else int(value)):
                res.append(i_list[i])
    elif operator == "<=":
        for i in range(len(i_list)):
            if (str(i_list[i][aoi]) if not num else int(i_list[i][aoi])) <= (str(value) if not num else int(value)):
                res.append(i_list[i])

    return res


def update_operator_handler(operator, ls, aoi, value, a_to_up, up_to):
    num = value.isnumeric()
    # keep track of the updated indexes
    indexes = []
    if operator == "==":
        for i in range(len(ls)):
            if (str(ls[i][aoi]) if not num else int(ls[i][aoi])) == (str(value) if not num else int(value)):
                # print(ls[i][a_to_up])
                ls[i][a_to_up] = up_to
                indexes.append(ls[i][0])
    elif operator == "!=":
        for i in range(len(ls)):
            if (str(ls[i][aoi]) if not num else int(ls[i][aoi])) != (str(value) if not num else int(value)):
                ls[i][a_to_up] = up_to
                indexes.append(ls[i][0])
    elif operator == ">=":
        for i in range(len(ls)):
            if (str(ls[i][aoi]) if not num else int(ls[i][aoi])) >= (str(value) if not num else int(value)):
                ls[i][a_to_up] = up_to
                indexes.append(ls[i][0])
    elif operator == ">":
        for i in range(len(ls)):
            if (str(ls[i][aoi]) if not num else int(ls[i][aoi])) > (str(value) if not num else int(value)):
                ls[i][a_to_up] = up_to
                indexes.append(ls[i][0])
    elif operator == "<=":
        for i in range(len(ls)):
            if (str(ls[i][aoi]) if not num else int(ls[i][aoi])) <= (str(value) if not num else int(value)):
                ls[i][a_to_up] = up_to
                indexes.append(ls[i][0])
    elif operator == "<":
        for i in range(len(ls)):
            if (str(ls[i][aoi]) if not num else int(ls[i][aoi])) < (str(value) if not num else int(value)):
                ls[i][a_to_up] = up_to
                indexes.append(ls[i][0])
    return ls, indexes


def check_argument_rules(argument):
    for i in range(len(argument)):
        if argument[i] in cons.banned_characters:
            # print("Banned character found")
            return True

    return False
