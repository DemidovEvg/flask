import random
from flask import Flask
from werkzeug.security import generate_password_hash
from project.database import db
from project.models import User, Truck


def register_commands(app: Flask):
    @app.cli.command("fill-db")
    def fill_db():
        session = db.session
        names = ['Ivanov', 'Petrov', 'Sidorov']
        new_users = []
        for i, current_name in enumerate(names):
            query_user_exists = (session.query(User)
                                        .filter(User.name == current_name)
                                        .exists())

            if session.query(query_user_exists).scalar():
                return
            new_users.append(
                User(
                    name=current_name,
                    email=f'{current_name}{i}@gmail.com',
                    password=generate_password_hash(
                        password='123',
                        method='sha256'
                    ),
                    experience=random.randint(0, 15)
                )
            )
        session.add_all(new_users)
        session.commit()

        users_ids = [u[0] for u in session.query(User.id).all()]
        marks = ['volvo', 'hyundai', 'unknown']
        new_trucks = []
        for i, current_mark in enumerate(marks, 1):
            new_trucks.append(
                Truck(
                    name=current_mark,
                    image_path=f'truck/{i}.jpg',
                    description="""Lorem Ipsum is simply dummy text of the printing 
                    and typesetting industry. Lorem Ipsum has been the industry's 
                    standard dummy text ever since the 1500s, when an unknown printer 
                    took a galley of type and scrambled it to make a type specimen book. 
                    It has survived not only five centuries, but also the leap 
                    into electronic typesetting, remaining essentially unchanged. 
                    It was popularised in the 1960s with the release of Letraset 
                    sheets containing Lorem Ipsum passages, and more recently 
                    with desktop publishing software like Aldus PageMaker
                    including versions of Lorem Ipsum.""",
                    driver_id=random.choice(users_ids)
                )
            )
        session.add_all(new_trucks)
        session.commit()
