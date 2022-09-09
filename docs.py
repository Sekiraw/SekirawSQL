import os

import constants as cons
import private_func as pf


class Document():
    def __init__(self, db, tables):
        self._db = db
        self._tables = tables

        self._rules = {}
        self._id = {}
        self._set_rules()

    def get_id(self, table):
        f = open(cons.db_folder + "/" + self._db + "/" + table + "_id.ini")
        res = f.read()
        f.close()
        return res

    def set_database(self, db, tables):
        self._rules.clear()
        self._id.clear()

        self._db = db
        self._tables = tables

        self._set_rules()

    def _set_rules(self):
        try:
            for i in self._tables:
                f = open(cons.db_folder + "/" + self._db + "/" + i + "_rules.ini")
                self._rules[i] = f.read()
                f.close()
            for i in self._tables:
                f = open(cons.db_folder + "/" + self._db + "/" + i + "_id.ini")
                self._id[i] = f.read()
                f.close()
        except FileNotFoundError:
            print("Table was not found!")
            del self

    def create_doc(self, argument, rules):
        doc = pf.get_loc(argument, self._db)
        if pf.check_argument_rules(argument):
            return cons.banned_error

        try:
            f = open(cons.db_folder + self._db + "/" + doc + ".ini", "w")
            f.write("")
            f.close()
            print("Document " + doc + " created successfully")
            f = open(cons.db_folder + "/" + self._db + "/" + doc + "_id.ini", "w")
            f.write(str(0))
            f.close()
            pf.create_doc_rules(self._db, doc, rules)
        except FileExistsError:
            print("Document " + doc + " already exists")

    def delete_doc(self, argument):
        doc = pf.get_loc(argument, self._db)
        if pf.check_argument_rules(argument):
            return cons.banned_error

        if os.path.exists(cons.db_folder + self._db + "/" + doc + ".ini"):
            os.remove(cons.db_folder + self._db + "/" + doc + ".ini")
            os.remove(cons.db_folder + self._db + "/" + doc + "_id.ini")
            os.remove(cons.db_folder + self._db + "/" + doc + "_rules.ini")
            print("Document " + doc + " deleted successfully")
        else:
            print("The document does not exist")

    def add(self, argument, test_run=False):
        doc = pf.get_loc(argument, self._db)
        if pf.check_argument_rules(argument):
            return cons.banned_error
        arg = argument.split(" ")
        # check the rules first
        rules = self._rules[doc]
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

        id = self._id[doc]
        data.insert(0, int(id) + 1)
        data = str(data).replace("'", "")
        print(data)

        if not test_run:
            f = open(cons.db_folder + "/" + self._db + "/" + doc + "_id.ini", "w")
            f.write(str(int(id) + 1))
            f.close()

            f = open(cons.db_folder + "/" + self._db + "/" + doc + ".ini", "a+")
            f.write(str(data) + ";")
            f.close()
        else:
            print("No errors were found. Test was successful!")
            return "No errors were found. Test was successful!"

    def get(self, argument):
        doc = pf.get_loc(argument, self._db)
        # if "LIMIT" in argument:
        #     limit = pf.limit(argument)
        if pf.check_argument_rules(argument):
            return cons.banned_error
        order = ""
        op_res, second, only = pf.operator_reader(argument)
        order, is_desc = pf.sort_operator_reader(argument)
        op_res = op_res.split("?")
        field = op_res[0]
        operator = op_res[1]
        value = op_res[2]

        # open and read the doc
        f = open(cons.db_folder + "/" + self._db + "/" + doc + ".ini", "r")
        data = f.read().split(';')
        f.close()
        # print(op_res)
        # open and read the rules
        rules = self._rules[doc]

        rules = rules.split(", ")

        aoi = -1
        aoi_order = -1 if order != "" else -2
        only_aoi = -2
        is_only = False
        for i in range(len(rules)):
            if only != "" and str(only) in str(rules[i]):
                only_aoi = i
                is_only = True
            if str(field) in str(rules[i]):
                aoi = i
            if order != "":
                if str(order) in str(rules[i]):
                    aoi_order = i

        # if aoi kept -1, that means there was no field in the rules that was given
        if aoi == -1:
            return "Field '" + str(field) + "' was not found in rules!"
        if aoi_order == -1:
            return "Field '" + str(order) + "' was not found in rules!"
        if only_aoi == -1:
            return "Field '" + str(only) + "' was not found in rules!"

        # print(aoi)
        ls = []
        # convert the string lists into lists
        for i in range(len(data)):
            ls.append(data[i].strip('][').split(', '))

        # print(ls)
        # print(len(ls))

        res = pf.operator_handler(operator, ls, aoi, value)

        # second query if there is an AND in the argument
        # it's ugly af, will fix it soon
        if second != "":
            n_res = pf.and_arg(doc, order, second, is_desc, res, self.get)

            if order != "":
                l = []
                res = pf.unique_sorter(n_res, aoi_order, l, is_desc if is_desc else False)
                if is_only:
                    if only_aoi != -1:
                        for i in range(len(res)):
                            res[i] = res[i][only_aoi]
                return res
            if is_only:
                if only_aoi != -1:
                    for i in range(len(n_res)):
                        n_res[i] = n_res[i][only_aoi]
            return n_res
        else:
            # if ORDER BY was found in the argument
            if order != "":
                l = []
                res = pf.unique_sorter(res, aoi_order, l, is_desc if is_desc else False)
            return res

    def update(self, argument, test_run=False):
        doc = pf.get_loc(argument, self._db)
        if pf.check_argument_rules(argument):
            return cons.banned_error

        op_res, second, _ = pf.operator_reader(argument)
        order, is_desc = pf.sort_operator_reader(argument)
        op_res = op_res.split("?")
        up_to, field_up_to = pf.update_to(argument)
        field = op_res[0]
        operator = op_res[1]
        value = op_res[2]

        f = open(cons.db_folder + "/" + self._db + "/" + doc + ".ini", "r")
        data = f.read().split(';')
        f.close()
        # print(op_res)
        rules = self._rules[doc]
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
        # print(len(ls))

        # custom part [LATER]
        if second != "":
            res = pf.operator_handler(operator, ls, aoi, value)
            n_res = pf.and_arg(doc, order, second, is_desc, res, self.get)
            # print(n_res)
            index = 0
            keep = n_res[0]
            for item, i in enumerate(ls):
                if i == keep:
                    index = item
            modified = n_res[0]
            modified[a_to_up] = up_to
            ls[index] = modified

            data_back = pf.datafy_list(ls)
            # print(data_back)
            if not test_run:
                f = open(cons.db_folder + "/" + self._db + "/" + doc + ".ini", "w")
                f.write(data_back)
                f.close()
                # print("Updated successfully!")
            else:
                print("No errors were found.")
                print("Test was successful!")
            return

        ls = pf.update_operator_handler(operator, ls, aoi, value, a_to_up, up_to)

        print(ls)

        # convert list to the unique string that the db uses
        data_back = pf.datafy_list(ls)
        # print(data_back)
        if not test_run:
            f = open(cons.db_folder + "/" + self._db + "/" + doc + ".ini", "w")
            f.write(data_back)
            f.close()
            print("Updated successfully!")
        else:
            print("No errors were found.")
            print("Test was successful!")
        # print(data_back)

    def delete(self, argument, test_run=False, recursion=False):
        doc = pf.get_loc(argument, self._db)
        if pf.check_argument_rules(argument):
            return cons.banned_error

        op_res, second, only = pf.operator_reader(argument)
        op_res = op_res.split("?")
        field = op_res[0]
        operator = op_res[1]
        value = op_res[2]
        if field == "" or operator == "" or value == "":
            print("Operator not found.")
            return

        f = open(cons.db_folder + "/" + self._db + "/" + doc + ".ini", "r")
        data = f.read().split(';')
        f.close()
        # print(op_res)
        rules = self._rules[doc]
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
        if second != "":
            val_second = self.delete("INDB " + self._db + " INTO " + doc + " WHERE " + second, test_run, True)
            merged = values_to_delete + val_second
            merged.sort()
            n_res = []
            aux = 0
            aux2 = 0
            for i in merged:
                aux2 = i
                if (aux2 == aux):
                    n_res.append(i)
                aux = i

            values_to_delete = n_res
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
            if recursion:
                return values_to_delete
            f = open(cons.db_folder + "/" + self._db + "/" + doc + ".ini", "w")
            f.write(res)
            f.close()
            print("Deleted successfully!")
        else:
            if recursion:
                return values_to_delete
            print("No errors were found.")
            print("Test was successful!")
        # print(data_back)

    def get_rules(self, document):
        try:
            print(self._rules[document])
        except KeyError:
            print(f"{document} was not found in rules")
