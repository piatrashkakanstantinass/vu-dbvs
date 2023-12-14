from typing import Optional
from dataclasses import dataclass
from tabulate import tabulate

from ..helper.db import get_cursor


@dataclass
class Post:
    post_id: int
    title: str
    content: str
    blog_id: int
    like_count: int
    dislike_count: int
    comment_count: int

    @staticmethod
    def get(blog_id_p):
        with get_cursor() as cursor:
            cursor.execute(
                """SELECT post_id,
                          title,
                          content,
                          blog_id,
                          like_count,
                          dislike_count,
                          comment_count
                   FROM PostsInfo
                   WHERE blog_id = %s""",
                (blog_id_p,),
            )
            posts = []
            for (
                post_id,
                title,
                content,
                blog_id,
                like_count,
                dislike_count,
                comment_count,
            ) in cursor.fetchall():
                posts.append(
                    Post(
                        post_id,
                        title,
                        content,
                        blog_id,
                        like_count,
                        dislike_count,
                        comment_count,
                    )
                )
            return posts

    @staticmethod
    def get_table(posts):
        headers = [
            "Title",
            "Content",
            "Like count",
            "Dislike count",
        ]
        rows = [
            (post.title, post.content, post.like_count, post.dislike_count)
            for post in posts
        ]
        return tabulate(rows, headers)

    @staticmethod
    def create(post):
        with get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO Posts (title, content, blog_id) VALUES (%s, %s, %s)",
                (post.title, post.content, post.blog_id),
            )
            cursor.connection.commit()

    @staticmethod
    def update(post):
        with get_cursor() as cursor:
            cursor.execute(
                "UPDATE Posts SET title = %s, content = %s WHERE post_id = %s",
                (post.title, post.content, post.post_id),
            )
            cursor.connection.commit()

    @staticmethod
    def delete(id):
        with get_cursor() as cursor:
            cursor.execute("DELETE FROM Posts WHERE post_id = %s", (id,))
            cursor.connection.commit()

    @staticmethod
    def like_dislike_count(id) -> tuple[int, int]:
        with get_cursor() as cursor:
            cursor.execute(
                "SELECT like_count, dislike_count FROM PostsInfo WHERE post_id = %s",
                (id,),
            )
            return cursor.fetchone()

    @staticmethod
    def post_reaction(id, user_id, likes: bool):
        with get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Reactions (post_id, user_id, likes) VALUES(%(post_id)s, %(user_id)s, %(likes)s)
                ON CONFLICT (user_id, post_id) DO UPDATE
                SET likes = EXCLUDED.likes
                """,
                {"post_id": id, "user_id": user_id, "likes": likes},
            )
            cursor.connection.commit()

    @staticmethod
    def remove_reaction(id, user_id):
        with get_cursor() as cursor:
            cursor.execute(
                "DELETE FROM Reactions WHERE user_id = %s AND post_id = %s",
                (user_id, id),
            )
            cursor.connection.commit()
