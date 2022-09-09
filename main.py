import random

import database as db
import docs as doc


if __name__ == '__main__':
    # db.create_database("school")
    # db.delete_database("asd")

    # create a document, the second argument is the rules
    # id field should always be given
    # doc.create_doc("CRDOC teachers INDB school", "id: int, name: string, age: int")
    # doc.delete_doc("DLDOC teachers INDB school")

    # prints the rules of the selected document
    # doc.get_rules("FROM students INDB school")

    # adds a list to the document with the selected values, the rules have to match
    # it ignores the values that are out of the range of the rules
    # If you give True to the second parameter it just runs a test, if it can be added or not
    # You don't have to give second parameter
    # The input field doest like spaces so "Kis Cica" should be "KisCica" will fix it later
    # doc.add("Miki,42 INDB school INTO teachers")
    # doc.add("NemMiki,18 INDB school INTO teachers", True)

    # returns the results as a list in list
    # the operators should be in between two questionmarks like >= should be ?>=?
    print(doc.get("INDB school FROM teachers WHERE age?>?21 AND name?==?Brigi"))
    # print(doc.get("INDB school FROM students WHERE id?==?4"))
    # AND operator can be used more than once
    # print(doc.get("INDB school FROM students WHERE age?>=?18 AND id?>?3"))
    # print(doc.get("INDB school FROM teachers WHERE age?>=?22 AND id?<?5 AND name?==?Filip"))

    # if you give a DESC keyword at the END of the argument it gives it back descending else ascending
    # it doesn't work on strings like names etc...
    # print(doc.get("INDB school FROM students WHERE age?>=?18 ORDER BY age DESC"))
    # python handles the "order by string" query's, by the length and alphabetical order
    # print(doc.get("INDB school FROM students WHERE age?>=?18 AND age?<=?40 ORDER BY name DESC"))
    # print(doc.get("INDB school FROM teachers WHERE age?>=?18 AND age?<=?40 ORDER BY age DESC ONLY name"))

    # doc.update("INDB school INTO teachers UPDATE name WHERE id?==?8 TO Mike")
    # doc.update(f"INDB slot1 INTO player UPDATE value WHERE stat?==?souls TO 250")

    # doc.delete("WHERE age?>=?18 INDB school FROM teachers")
    # doc.delete("INDB school FROM teachers WHERE age?>=18? AND name?!=?Brigi")

    # example
    # names = ["FenellaBuxton", "AdnaanSquires", "VincenzoBlankenship", "CarloBaird", "MacPayne", "KomalGoodman"]
    # auth = "admin"
    # age = 0
    # for i in range(6):
    #     age = random.randint(20, 50)
    #     doc.add(str(names[i]) + "," + str(age) + "," + str(auth) + " INDB company INTO admins")

    # doc.update(f"INDB slot1 INTO doors UPDATE islocked WHERE doorid?==?map2-1 TO 0")

    # querry = doc.get(f"INDB slot1 FROM ground_objects WHERE map?==?map2-1 AND groundid?==?0")
    # print(querry)

    # doc.update(f"INDB slot1 INTO ground_objects UPDATE ispickedup WHERE itemid?==?201 TO 70")

    # doc.update(f"INDB slot1 INTO weapon_inv UPDATE slotindex WHERE customid?==?5 TO 0")


