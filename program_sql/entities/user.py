from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from tabulate import tabulate

from ..helper.db import get_cursor


@dataclass
class User:
    user_id: int
    username: str
    email: str
    created_at: datetime
    first_name: Optional[str]
    last_name: Optional[str]
    user_status: str = "OK"

    @staticmethod
    def create():
        return User()

    @staticmethod
    def get():
        with get_cursor() as cursor:
            cursor.execute(
                """SELECT user_id,
                          username,
                          email,
                          first_name,
                          last_name,
                          user_status,
                          created_at
                   FROM Users"""
            )
            users = []
            for (
                user_id,
                username,
                email,
                first_name,
                last_name,
                user_status,
                created_at,
            ) in cursor.fetchall():
                users.append(
                    User(
                        user_id,
                        username,
                        email,
                        created_at,
                        first_name,
                        last_name,
                        user_status,
                    )
                )
            return users

    @staticmethod
    def get_table(users):
        headers = [
            "Username",
            "Email",
            "First name",
            "Last name",
            "Status",
            "Created at",
        ]
        rows = [
            (
                user.username,
                user.email,
                user.first_name,
                user.last_name,
                user.user_status,
                user.created_at,
            )
            for user in users
        ]
        return tabulate(rows, headers)

    @staticmethod
    def create(user):
        with get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO Users (username, email, first_name, last_name, user_status) VALUES (%s, %s, %s, %s, %s)",
                (
                    user.username,
                    user.email,
                    user.first_name,
                    user.last_name,
                    user.user_status,
                ),
            )
            cursor.connection.commit()

    @staticmethod
    def update(user):
        with get_cursor() as cursor:
            cursor.execute(
                "UPDATE Users SET username = %s, email = %s, first_name = %s, last_name = %s, user_status = %s WHERE user_id = %s",
                (
                    user.username,
                    user.email,
                    user.first_name,
                    user.last_name,
                    user.user_status,
                    user.user_id,
                ),
            )
            cursor.connection.commit()

    @staticmethod
    def delete(id):
        with get_cursor() as cursor:
            cursor.execute("SELECT blog_id FROM Blogs WHERE user_id = %s", (id,))
            blogs = cursor.fetchall()
            for blog in blogs:
                cursor.execute("DELETE FROM Posts WHERE blog_id = %s", blog)
            cursor.execute("DELETE FROM Blogs WHERE user_id = %s", (id,))
            cursor.execute("DELETE FROM Users WHERE user_id = %s", (id,))
            cursor.connection.commit()
