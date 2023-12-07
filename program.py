import questionary
from tabulate import tabulate
import psycopg2
from typing import Optional, Callable, Tuple
from dotenv import load_dotenv
import os

load_dotenv()

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
# dbname = studentu host=pgsql3.mif passowrd=pswd


class DBContext:
    def __enter__(self):
        self.conn = psycopg2.connect(CONNECTION_STRING)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.conn.close()


def db_create_user(username: str, email: str):
    with DBContext() as cursor:
        cursor.execute(
            "INSERT INTO Users (username, email) VALUES (%s, %s)", (username, email)
        )
        cursor.connection.commit()


def db_list_users(username: Optional[str] = None):
    with DBContext() as cursor:
        if username == None:
            cursor.execute(
                "SELECT username, email, first_name, last_name, user_status FROM Users"
            )
        else:
            cursor.execute(
                "SELECT username, email, first_name, last_name, user_status FROM Users WHERE username = %s",
                (username,),
            )
        entries = cursor.fetchall()
    return entries


def db_delete_user(username: str):
    with DBContext() as cursor:
        cursor.execute("DELETE FROM Users WHERE username = %s", (username,))
        cursor.connection.commit()


def db_update_user_flag(username: str, flag: str):
    with DBContext() as cursor:
        cursor.execute(
            "UPDATE Users SET user_status = %s WHERE username = %s", (flag, username)
        )
        cursor.connection.commit()


def db_udpate_user(
    username: str, new_email: str, new_first_name: str, new_last_name: str
):
    with DBContext() as cursor:
        cursor.execute(
            "UPDATE Users SET email = %s, first_name = %s, last_name = %s WHERE username = %s",
            (new_email, new_first_name, new_last_name, username),
        )
        cursor.connection.commit()


def db_list_usernames():
    with DBContext() as cursor:
        cursor.execute("SELECT username from Users")
        return cursor.fetchall()


def create_user():
    username = questionary.text("Pick username:").unsafe_ask()
    email = questionary.text("Pick email:").unsafe_ask()
    db_create_user(username, email)
    questionary.print("User created")


def list_users():
    print_users(db_list_users())


def confirm_user() -> Optional[str]:
    username = questionary.text("Which user? (username)").unsafe_ask()
    found_users = db_list_users(username)
    if len(found_users) == 0:
        questionary.print("No user found")
        return
    print_users(found_users)
    res = questionary.confirm("Confirm?").unsafe_ask()
    return username if res else None


def print_users(users):
    table = tabulate(
        users,
        headers=["username", "email", "First name", "Second name", "Status"],
    )
    questionary.print(table)


def delete_user():
    username = confirm_user()
    if username == None:
        return
    db_delete_user(username)
    questionary.print("Deleted")


def update_user():
    username = confirm_user()
    if username == None:
        return
    (
        curr_username,
        curr_email,
        curr_first_name,
        curr_last_name,
        user_status,
    ) = db_list_users(username)[0]
    new_email = questionary.text("New email?", default=curr_email).unsafe_ask()
    new_first_name = questionary.text(
        "New first name?", default=curr_first_name
    ).unsafe_ask()
    new_last_name = questionary.text(
        "New last name?", default=curr_last_name
    ).unsafe_ask()
    db_udpate_user(username, new_email, new_first_name, new_last_name)
    questionary.print("Updated")


def handle_flag_change(new_value):
    username = confirm_user()
    if username == None:
        return
    db_update_user_flag(username, new_value)
    questionary.print("Updated")


def flag_user():
    handle_flag_change("FLAGGED")


def unflag_user():
    handle_flag_change("OK")


class OptionMenu:
    options: list[Tuple[str, Callable]]
    message: str

    EXIT_OPTION = "exit menu"

    def __init__(self, message: str):
        self.message = message
        self.options = []

    def add_option(self, label: str, callback: Callable):
        self.options.append((label, callback))

    def display_menu(self):
        choices = [label for label, _ in self.options] + [self.EXIT_OPTION]
        while True:
            selected_label = questionary.select(self.message, choices).unsafe_ask()
            if selected_label == self.EXIT_OPTION or selected_label == None:
                break
            for label, callback in self.options:
                if label == selected_label:
                    callback()


def db_create_blog(blog_name: str, blog_description: str, username: str):
    with DBContext() as cursor:
        cursor.execute(
            """
            INSERT INTO Blogs (blog_name, blog_description, user_id)
            VALUES (%s, %s, %s)
            """,
            (blog_name, blog_description, user_id),
        )
        cursor.connection.commit()


# def db_list_blogs(username: Optional[int] = None):
#     with DBContext() as cursor:
#         if user_id is None:
#             cursor.execute(
#                 "SELECT blog_id, blog_name, blog_description, blog_status, created_at FROM Blogs"
#             )
#         else:
#             cursor.execute(
#                 """
#                 SELECT blog_id, blog_name, blog_description, blog_status, created_at
#                 FROM Blogs
#                 WHERE user_id = %s
#                 """,
#                 (user_id,),
#             )
#         entries = cursor.fetchall()
#     return entries


# def db_update_blog(blog_id: int, new_name: str, new_description: str):
#     with DBContext() as cursor:
#         cursor.execute(
#             """
#             UPDATE Blogs
#             SET blog_name = %s, blog_description = %s
#             WHERE blog_id = %s
#             """,
#             (new_name, new_description, blog_id),
#         )
#         cursor.connection.commit()


# def db_delete_blog(blog_id: int):
#     with DBContext() as cursor:
#         cursor.execute("DELETE FROM Blogs WHERE blog_id = %s", (blog_id,))
#         cursor.connection.commit()


def pick_username():
    usernames = [user for user, in db_list_usernames()]
    return questionary.select("Pick user", usernames).unsafe_ask()


def create_blog():
    username = pick_username()
    blog_name = questionary.text("Enter blog name:").unsafe_ask()
    blog_description = questionary.text("Enter blog description:").unsafe_ask()
    db_create_blog(blog_name, blog_description, username)
    questionary.print("Blog created")


blog_options_menu = OptionMenu("Blog actions")
blog_options_menu.add_option("create blog", create_blog)


top_level_options_menu = OptionMenu("Choose action")
top_level_options_menu.add_option("create user", create_user)
top_level_options_menu.add_option("list users", list_users)
top_level_options_menu.add_option("delete user", delete_user)
top_level_options_menu.add_option("update user info", update_user)
top_level_options_menu.add_option("flag user", flag_user)
top_level_options_menu.add_option("unflag user", unflag_user)
top_level_options_menu.add_option("blog actions...", blog_options_menu.display_menu)


if __name__ == "__main__":
    while True:
        try:
            top_level_options_menu.display_menu()
            break
        except KeyboardInterrupt:
            questionary.print("Exiting")
            break
        except psycopg2.errors.CheckViolation:
            questionary.print(
                "Failed value check (perhaps value already exists or must satisfy certain requirements)"
            )
            continue
        except psycopg2.errors.ForeignKeyViolation:
            questionary.print(
                "Failed to perform action. Some entities depend on object and should be changed first"
            )
            continue
