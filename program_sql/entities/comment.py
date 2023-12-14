from dataclasses import dataclass
from tabulate import tabulate
from datetime import datetime

from ..helper.db import get_cursor


@dataclass
class Comment:
    comment_id: int
    content: str
    user_id: str
    post_id: int
    username: str
    created_at: datetime

    @staticmethod
    def get(post_id_p):
        with get_cursor() as cursor:
            cursor.execute(
                """SELECT comment_id,
                          content,
                          Comments.user_id,
                          post_id,
                          username,
                          Comments.created_at
                   FROM Comments
                   JOIN Users ON Comments.user_id = Users.user_id
                   WHERE post_id = %s""",
                (post_id_p,),
            )
            comments = []
            for (
                comment_id,
                content,
                user_id,
                post_id,
                username,
                created_at,
            ) in cursor.fetchall():
                comments.append(
                    Comment(comment_id, content, user_id, post_id, username, created_at)
                )
            return comments

    @staticmethod
    def get_table(comments):
        headers = [
            "Content",
            "Username",
            "Created at",
        ]
        rows = [
            (comment.content, comment.username, comment.created_at)
            for comment in comments
        ]
        return tabulate(rows, headers)

    @staticmethod
    def create(comment):
        with get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO Comments (content, user_id, post_id) VALUES (%s, %s, %s)",
                (comment.content, comment.user_id, comment.post_id),
            )
            cursor.connection.commit()

    @staticmethod
    def update(comment):
        with get_cursor() as cursor:
            cursor.execute(
                "UPDATE Comments SET content = %s WHERE comment_id = %s",
                (comment.content, comment.comment_id),
            )
            cursor.connection.commit()

    @staticmethod
    def delete(id):
        with get_cursor() as cursor:
            cursor.execute("DELETE FROM Comments WHERE comment_id = %s", (id,))
            cursor.connection.commit()
