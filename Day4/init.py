from app import app, db
from models import User


users = [
    ('u1', 'email1', 'p1'),
    ('u2', 'email2', 'p2'),
    ('u3', 'email3', 'p3'),
]

creators = [
    ('c1', 'c_email1', 'p1'),
    ('c2', 'c_email2', 'p2'),
    ('c3', 'c_email3', 'p3'),
]

a = User(name='admin', email='adminemail', password='p', isAdmin=True)
db.session.add(a)
db.session.commit()

for (name, email, password) in users:
    u = User(name=name, email=email, password=password)
    db.session.add(u)
    db.session.commit()

for (name, email, password) in creators:
    u = User(name=name, email=email, password=password, isCreator=True)
    db.session.add(u)
    db.session.commit()