from app import db, User

username = "admin"
password = "admin1234"
level = "Admin"
db.session.add(User(username, password, level))
db.session.commit()