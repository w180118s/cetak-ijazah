from app import db, Konsumen

username = "konsumen1"
password = "12345"
level = "konsumen"
db.session.add(Konsumen(username, password, level))
db.session.commit()