import random

import database as db
import docs as doc


if __name__ == '__main__':
    # db.create_database("school")
    # db.delete_database("asd")

    # id field should always be given
    # doc.create_doc("CRDOC teachers INDB school", "id: int, name: string, age: int")
    # doc.delete_doc("DLDOC teachers INDB school")

    # prints the rules of the selected document
    # doc.get_rules("FROM students INDB school")

    # adds a list to the document with the selected values, the rules have to match
    # it ignores the values that are out of the range of the rules
    # so if I would give it Cica,22,54 <- the 54 couldn't be used
    # The input field doest like spaces so "Kis Cica" should be "KisCica" will fix it later
    # doc.add("Cica,18 INDB school INTO students")

    # returns the results as a list in list
    # print(doc.get("INDB school FROM students WHERE age?>?21"))
    # print(doc.get("INDB school FROM students WHERE id?==?4"))
    # print(doc.get("INDB school FROM students WHERE name?==?Pablo"))

    doc.update("INDB school INTO students UPDATE name WHERE id?==?4 TO Filip")

    # doc.delete("WHERE name?==?Pablo INDB school FROM students")

    # example
    # names = ["FenellaBuxton", "AdnaanSquires", "VincenzoBlankenship", "CarloBaird", "MacPayne", "KomalGoodman"]
    # auth = "admin"
    # age = 0
    # for i in range(6):
    #     age = random.randint(20, 50)
    #     doc.add(str(names[i]) + "," + str(age) + "," + str(auth) + " INDB users INTO admins")
