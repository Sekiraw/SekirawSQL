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

    def get_database(self):
        return self._db

    def get_tables(self):
        return self._tables

    def get_ids(self):
        return self._id

    def get_id(self, doc):
        path = ''.join([cons.db_folder, self._db, '/', doc, '_id.ini'])
        if os.path.exists(path):
            f = open(path, 'r')
            res = f.read()
            f.close()
            return res
        return ''.join(["Document ", doc, "doesn't exists"])

    def set_database(self, db, tables):
        self._rules.clear()
        self._id.clear()

        self._db = db
        self._tables = tables

        self._set_rules()

    def _set_rules(self):
        try:
            for i in self._tables:
                f = open(''.join([cons.db_folder, self._db, '/', i, '_rules.ini']), 'r')
                self._rules[i] = f.read()
                f.close()

                f = open(''.join([cons.db_folder, self._db, '/', i, '_id.ini']), 'r')
                self._id[i] = f.read()
                f.close()
        except IOError as e:
            print(e)

    def create_doc(self, argument, rules):
        argument = argument.split(' ')
        doc = pf.get_loc(argument, self._db)
        if pf.check_argument_rules(argument):
            return cons.banned_error

        path = ''.join([cons.db_folder, self._db, '/', doc, '.ini'])
        if os.path.exists(path):
            print(''.join(["Document ", doc, " already exists"]))
            return

        try:
            f = open(path, 'w')
            f.write('')
            f.close()

            f = open(''.join([cons.db_folder, self._db, '/', doc, '_id.ini']), 'w')
            f.write(str(0))
            f.close()

            f = open(''.join([cons.db_folder, self._db, '/', doc, '_rules.ini']), 'w')
            f.write('id: int, ' + rules)
            f.close()
        except IOError as e:
            print(e)
            return

        print('Document created successfully')

    def delete_doc(self, argument):
        argument = argument.split(' ')
        doc = pf.get_loc(argument, self._db)
        if pf.check_argument_rules(argument):
            return cons.banned_error

        doc_path = ''.join([cons.db_folder, self._db, '/', doc, '.ini'])
        try:
            os.remove(doc_path)
            os.remove(''.join([cons.db_folder, self._db, '/', doc, '_id.ini']))
            os.remove(''.join([cons.db_folder, self._db, '/', doc, '_rules.ini']))
            print(''.join(["Document ", doc, " deleted successfully"]))
            return
        except IOError as e:
            print(e)

        print("Document does not exist")

    def add(self, argument, test_run=False):
        argument = argument.split(' ')
        doc = pf.get_loc(argument, self._db)
        if pf.check_argument_rules(argument):
            return cons.banned_error
        # check the rules first
        rules = self._rules[doc]
        rules = rules.replace(" ", "")
        rules = rules.split(",")
        rules.pop(0)

        data = argument[0].split(",")

        for i in range(len(rules)):
            if "int" in rules[i]:
                if not data[i].isnumeric():
                    print("Inserted value doesn't match the rules")
                if len(data) != len(rules):
                    print(''.join(["Given values doesn't match the rules \nRules: ", str(rules)]))
        print("Rules match! Inserting data.")

        id = self._id[doc]
        self._id[doc] = int(self._id[doc]) + 1
        data.insert(0, int(id) + 1)
        data = str(data).replace("'", "")
        print(data)

        if not test_run:
            f = open(''.join([cons.db_folder, self._db, '/', doc, '_id.ini']), 'w')
            f.write(str(int(id) + 1))
            f.close()

            f = open(''.join([cons.db_folder, self._db, '/', doc, '.ini']), 'a+')
            f.write(str(data) + ';')
            f.close()
        else:
            print("No errors were found. Test was successful!")

    def get(self, argument):
        argument = argument.split(' ')
        doc = pf.get_loc(argument, self._db)
        # if "LIMIT" in argument:
        #     limit = pf.limit(argument)
        if pf.check_argument_rules(argument):
            return cons.banned_error
        order = ""
        op_res, second, only = pf.operator_reader(argument)
        order, is_desc = pf.sort_operator_reader(argument)
        op_res = op_res.split('?')
        field = op_res[0]
        operator = op_res[1]
        value = op_res[2]

        # open and read the doc
        f = open(''.join([cons.db_folder, self._db, '/', doc, '.ini']), 'r')
        data = f.read().split(';')
        f.close()
        # set the rules
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
            return ''.join(["Field '", str(field), "' was not found in rules!"])
        if aoi_order == -1:
            return ''.join(["Field '", str(order), "' was not found in rules!"])
        if only_aoi == -1:
            return ''.join(["Field '", str(only), "' was not found in rules!"])

        ls = []
        # convert the string lists into lists
        for i in range(len(data)):
            ls.append(data[i].strip('][').split(', '))
        ls.pop(-1)

        res = pf.operator_handler(operator, ls, aoi, value)

        if len(second) > 0:
            result = []
            for i in second:
                i = i.split('?')
                sec_field = i[0]
                sec_operator = i[1]
                sec_value = i[2]
                sec_aoi = -1

                for i in range(len(rules)):
                    if str(sec_field) in str(rules[i]):
                        sec_aoi = i

                res = pf.operator_handler(sec_operator, res, sec_aoi, sec_value)

            for i in res:
                result.append(i)
            res = result

        if order != "":
            l = []
            res = pf.unique_sorter(res, aoi_order, l, is_desc if is_desc else False)
            if is_only:
                if only_aoi != -1:
                    for i in range(len(res)):
                        res[i] = res[i][only_aoi]

        if is_only:
            if only_aoi != -1:
                for i in range(len(res)):
                    res[i] = res[i][only_aoi]

        return res

    def update(self, argument, test_run=False):
        argument = argument.split(' ')
        doc = pf.get_loc(argument, self._db)
        if pf.check_argument_rules(argument):
            return cons.banned_error

        op_res, second, _ = pf.operator_reader(argument)
        op_res = op_res.split('?')
        up_to, field_up_to = pf.update_to(argument)
        field = op_res[0]
        operator = op_res[1]
        value = op_res[2]

        doc_path = ''.join([cons.db_folder, self._db, '/', doc, '.ini'])
        f = open(doc_path, 'r')
        data = f.read().split(';')
        f.close()

        rules = self._rules[doc]
        rules = rules.split(", ")

        aoi = -1
        a_to_up = -1
        for i in range(len(rules)):
            if str(field) in str(rules[i]):
                aoi = i

        if aoi == -1:
            return ''.join(["Field '", str(field), "' was not found in rules!"])

        for i in range(len(rules)):
            if str(field_up_to) in str(rules[i]):
                a_to_up = i

        if a_to_up == -1:
            return ''.join(["Field '", str(field_up_to), "' was not found in rules!"])

        ls = []
        # convert the string lists into lists
        for i in range(len(data)):
            ls.append(data[i].strip('][').split(', '))
        ls.pop(-1)

        res = pf.operator_handler(operator, ls, aoi, value)

        if len(second) > 0:
            result = []
            for i in second:
                i = i.split('?')
                sec_field = i[0]
                sec_operator = i[1]
                sec_value = i[2]
                sec_aoi = -1

                for i in range(len(rules)):
                    if str(sec_field) in str(rules[i]):
                        sec_aoi = i

                # overwriting the res to restrict the list as the restrictions require
                res = pf.operator_handler(sec_operator, res, sec_aoi, sec_value)

            for i in res:
                result.append(i)

            operator_result_list, updated_indexes = pf.update_operator_handler(operator, result, aoi, value, a_to_up, up_to)

            # we've got the indexes of the updated elements from the operator handler,
            # so if i[0]-th element is in the index list (index list holds the ids of the updatde elements),
            # because it's in order, we overwrite ls[i] to the operator result list's [0]-th element
            # and dereference it from the op_res_list, so we can still follow the order
            # it is a faster solution than going through ls and op_r_l as i and j
            for i in ls:
                if i[0] in updated_indexes:
                    i = operator_result_list[0]
                    del operator_result_list[0]

        else:
            # if there is no AND statement, we don't have to restrict the list
            ls, _ = pf.update_operator_handler(operator, ls, aoi, value, a_to_up, up_to)

        if not test_run:
            f = open(doc_path, 'w')
            f.write(pf.datafy_list(ls))
            f.close()
            # print("Updated successfully!")
        else:
            print("Test was successful!")

    def delete(self, argument, test_run=False):
        argument = argument.split(' ')
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

        doc_path = ''.join([cons.db_folder, self._db, '/', doc, '.ini'])
        f = open(doc_path, 'r')
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
            return ''.join(["Field '", str(field), "' was not found in rules!"])

        # print(aoi)
        # print(a_to_up)
        ls = []
        # convert the string lists into lists
        for i in range(len(data)):
            ls.append(data[i].strip('][').split(', '))
        ls.pop(-1)

        values_to_delete = pf.operator_handler(operator, ls, aoi, value)

        result = []
        if len(second) > 0:
            for i in second:
                i = i.split('?')
                sec_field = i[0]
                sec_operator = i[1]
                sec_value = i[2]
                sec_aoi = -1

                for i in range(len(rules)):
                    if str(sec_field) in str(rules[i]):
                        sec_aoi = i

                values_to_delete = pf.operator_handler(sec_operator, values_to_delete, sec_aoi, sec_value)

            for i in values_to_delete:
                result.append(i)
            values_to_delete = result

        for i in values_to_delete:
            ls.remove(i)

        if not test_run:
            f = open(doc_path, 'w')
            f.write(pf.datafy_list(ls))
            f.close()
            print("Deleted successfully!")
        else:
            print("Test was successful!")
        # print(data_back)

    def get_rules(self, document):
        try:
            print(self._rules[document])
        except KeyError:
            print(''.join([document, " was not found in rules"]))
