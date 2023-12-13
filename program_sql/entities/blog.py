from typing import Optional
from dataclasses import dataclass
from tabulate import tabulate

from ..helper.db import get_cursor


@dataclass
class Blog:
    blog_id: int
    blog_name: str
    user_id: int
    username: str
    blog_status: str = "OPEN"
    blog_description: Optional[str] = None

    @staticmethod
    def get(user_id_p):
        with get_cursor() as cursor:
            cursor.execute(
                """SELECT blog_id,
                          blog_name,
                          blog_status,
                          Blogs.user_id,
                          username,
                          blog_description
                   FROM Blogs
                   JOIN Users ON Users.user_id = Blogs.user_id
                   WHERE Blogs.user_id = %s""",
                (user_id_p,),
            )
            blogs = []
            for (
                blog_id,
                blog_name,
                blog_status,
                user_id,
                username,
                blog_description,
            ) in cursor.fetchall():
                blogs.append(
                    Blog(
                        blog_id,
                        blog_name,
                        user_id,
                        username,
                        blog_status,
                        blog_description,
                    )
                )
            return blogs

    @staticmethod
    def get_table(blogs):
        headers = [
            "Blog",
            "Status",
            "Owner",
            "Description",
        ]
        rows = [
            (blog.blog_name, blog.blog_status, blog.username, blog.blog_description)
            for blog in blogs
        ]
        return tabulate(rows, headers)

    @staticmethod
    def create(blog):
        with get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO Blogs (blog_name, blog_description, blog_status, user_id) VALUES (%s, %s, %s, %s)",
                (
                    blog.blog_name,
                    blog.blog_description,
                    blog.blog_status,
                    blog.user_id,
                ),
            )
            cursor.connection.commit()

    @staticmethod
    def update(blog):
        with get_cursor() as cursor:
            cursor.execute(
                "UPDATE Blogs SET blog_name = %s, blog_description = %s, blog_status = %s WHERE blog_id = %s",
                (blog.blog_name, blog.blog_description, blog.blog_status, blog.blog_id),
            )
            cursor.connection.commit()

    @staticmethod
    def delete(id):
        with get_cursor() as cursor:
            cursor.execute("DELETE FROM Posts WHERE blog_id = %s", (id,))
            cursor.execute("DELETE FROM Blogs WHERE blog_id = %s", (id,))
            cursor.connection.commit()
