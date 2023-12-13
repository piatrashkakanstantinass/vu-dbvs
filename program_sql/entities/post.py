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

    @staticmethod
    def get(blog_id_p):
        with get_cursor() as cursor:
            cursor.execute(
                """SELECT post_id,
                          title,
                          content,
                          blog_id,
                          COUNT(DISTINCT r1.user_id),
                          COUNT(DISTINCT r2.user_id)
                   FROM Posts
                   JOIN Blogs ON Posts.blog_id = Blogs.blog_id
                   LEFT JOIN Reactions r1 ON r1.post_id = Posts.post_id
                   LEFT JOIN Reactions r2 ON r2.post_id = Posts.post_id
                   WHERE Posts.blog_id = %s
                   AND r1.likes = TRUE
                   AND r2.likes = FALSE""",
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
            ) in cursor.fetchall():
                posts.append(
                    Post(post_id, title, content, blog_id, like_count, dislike_count)
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
