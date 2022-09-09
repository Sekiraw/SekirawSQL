import constants as cons
from pathlib import Path


def create_doc_rules(db, doc, rules):
    f = open(''.join([cons.db_folder, db, '/', doc, '_rules.ini']), 'w')
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
def get_loc(arg, db):
    doc = ""
    arg = arg.split(' ')
    for i in range(len(arg)):
        if "INTO" in arg[i]:
            doc = str(arg[i + 1])
        if "CRDOC" in arg[i]:
            doc = str(arg[i + 1])
        if "DLDOC" in arg[i]:
            doc = str(arg[i + 1])
        if "FROM" in arg[i]:
            doc = str(arg[i + 1])
    if doc == "":
        print("Something went wrong")
        return

    # check if file exists
    location = Path(''.join([cons.db_folder, db, '/', doc, '.ini']))
    if location.exists():
        return doc
    else:
        print("Cannot find document.")
        return doc


def limit(argument):
    # don't split it if it's not even in there
    limit = 0
    arg = argument.split(' ')
    for i in range(len(arg)):
        if arg[i] == "LIMIT":
            limit = arg[i+1]
    return limit


def operator_reader(arg):
    arg = arg.split(" ")
    where = ""
    andd = ""
    only = ""
    for i in range(len(arg)):
        if "WHERE" in arg[i]:
            where = arg[i+1]
        if "AND" in arg[i]:
            andd = arg[i+1]
        if "ONLY" in arg[i]:
            only = arg[i+1]

    if where == "":
        print("Error, operator was not found!")
        return
    else:
        return where, andd, only


def sort_operator_reader(argument):
    parameter = ""
    desc = False
    arg = argument.split(" ")
    for i in range(len(arg)):
        if arg[i] == "ORDER" and arg[i+1] == "BY":
            parameter = arg[i+2]
        if arg[i] == "DESC":
            desc = True

    return parameter, desc


# had to make it recursive, sorry memory
def unique_sorter(ls, aoi, res, rev=False):
    if len(ls) == 0:
        if rev:
            res.reverse()
            return res
        return res

    min = ls[-1]
    for i in range(len(ls)):
        if ls[i][aoi] < min[aoi]:
            min = ls[i]

    res.append(min)
    ls.remove(min)
    return unique_sorter(ls, aoi, res, rev)


def and_arg(doc, order, second, is_desc, res, get):
    if order == "":
        second_get = get(''.join(["FROM ", doc, " WHERE ", second]))
    else:
        desc = ""
        if is_desc:
            desc = " DESC"
        second_get = get(''.join(["FROM ", doc, " WHERE ", second, " ORDER BY ", order, desc]))

    merged = res + second_get
    merged.sort()
    # if limit != -1:
    #     merged = merged[1]
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


def and_arg_no_order(db, doc, second, res, delete):
    second_delete = delete(''.join(["FROM ", doc, " WHERE ", second]))
    merged = res + second_delete
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


def operator_handler(operator, list, aoi, value):
    res = []
    num = value.isnumeric()
    if operator == "==":
        for i in range(len(list) - 1):
            if (str(list[i][aoi]) if not num else int(list[i][aoi])) == (str(value) if not num else int(value)):
                res.append(list[i])
    elif operator == "!=":
        for i in range(len(list)-1):
            if (str(list[i][aoi]) if not num else int(list[i][aoi])) != (str(value) if not num else int(value)):
                res.append(list[i])
    elif operator == ">":
        for i in range(len(list)-1):
            if (str(list[i][aoi]) if not num else int(list[i][aoi])) > (str(value) if not num else int(value)):
                # print(list[i][aoi], ">", value)
                res.append(list[i])
    elif operator == "<":
        for i in range(len(list)-1):
            if (str(list[i][aoi]) if not num else int(list[i][aoi])) < (str(value) if not num else int(value)):
                res.append(list[i])
    elif operator == ">=":
        for i in range(len(list)-1):
            if (str(list[i][aoi]) if not num else int(list[i][aoi])) >= (str(value) if not num else int(value)):
                res.append(list[i])
    elif operator == "<=":
        for i in range(len(list)-1):
            if (str(list[i][aoi]) if not num else int(list[i][aoi])) <= (str(value) if not num else int(value)):
                res.append(list[i])

    return res


def update_operator_handler(operator, ls, aoi, value, a_to_up, up_to):
    num = value.isnumeric()
    if operator == "==":
        for i in range(len(ls) - 1):
            if (str(ls[i][aoi]) if not num else int(ls[i][aoi])) == (str(value) if not num else int(value)):
                # print(ls[i][a_to_up])
                ls[i][a_to_up] = up_to
    elif operator == "!=":
        for i in range(len(ls) - 1):
            if (str(ls[i][aoi]) if not num else int(ls[i][aoi])) != (str(value) if not num else int(value)):
                ls[i][a_to_up] = up_to
    elif operator == ">=":
        for i in range(len(ls) - 1):
            if (str(ls[i][aoi]) if not num else int(ls[i][aoi])) >= (str(value) if not num else int(value)):
                ls[i][a_to_up] = up_to
    elif operator == ">":
        for i in range(len(ls) - 1):
            if (str(ls[i][aoi]) if not num else int(ls[i][aoi])) > (str(value) if not num else int(value)):
                ls[i][a_to_up] = up_to
    elif operator == "<=":
        for i in range(len(ls) - 1):
            if (str(ls[i][aoi]) if not num else int(ls[i][aoi])) <= (str(value) if not num else int(value)):
                ls[i][a_to_up] = up_to
    elif operator == "<":
        for i in range(len(ls) - 1):
            if (str(ls[i][aoi]) if not num else int(ls[i][aoi])) < (str(value) if not num else int(value)):
                ls[i][a_to_up] = up_to
    return ls


def check_argument_rules(argument):
    for i in range(len(argument)):
        if argument[i] in cons.banned_characters:
            # print("Banned character found")
            return True

    return False