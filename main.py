import database as db
import docs as doc


if __name__ == '__main__':
    # db.create_database("school")
    # db.delete_database("asd")
    # doc.create_doc("CRDOC teachers INDB school", "id: int, name: string, age: int")
    # doc.delete_doc("DLDOC teachers INDB school")
    # doc.add("Peti,21 INDB school INTO students")
    doc.get("INDB school FROM students WHERE id?==?2")
