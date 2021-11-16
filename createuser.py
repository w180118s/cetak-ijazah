from app import db, User

username = "admin"
password = "12345"
level = "Admin"
db.session.add(User(username, password, level))
db.session.commit()
