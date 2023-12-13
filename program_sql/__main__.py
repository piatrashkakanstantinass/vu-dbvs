"""
blog actions

blog actions
select whose blog you are viewing

  list blogs
  create blog
  update blog
  delete blog

post actions
select which blog

  list posts
  create post
  update post
  delete post

post actions
selct which post

comments
  list comments
  create comment (get username)
  update comment
  delete comment

"""

from .helper.menu import Menu
from .helper import prompts

from .entities.user import User


def create_user(state):
    user = user_prompt()
    User.create(user)


def update_user(state):
    user = pick_user()
    if user == None:
        return
    new_user = user_prompt(user)
    new_user.user_id = user.user_id
    User.update(new_user)


def delete_user(state):
    user = pick_user()
    if user == None:
        return
    User.delete(user.user_id)


def user_prompt(user=None):
    username = prompts.inputUsername(user.username)
    email = prompts.inputMandatory("Pick email", user.email)
    first_name = prompts.inputOptional("Pick first name", user.first_name)
    last_name = prompts.inputOptional("Pck last name", user.last_name)
    user_status = prompts.select("Pick status", ["OK", "CLOSED", "FLAGGED"])
    return User(0, username, email, 0, first_name, last_name, user_status)


def pick_user():
    users = User.get()
    usernames = [user.username for user in users]
    username = prompts.select("Pick user", usernames)
    if username == None:
        return
    for user in users:
        if user.username == username:
            return user


user_actions_menu = Menu()
user_actions_menu.add_option("list users", lambda s: print(User.get_table(User.get())))
user_actions_menu.add_option("create user", create_user)
user_actions_menu.add_option("update user", update_user)
user_actions_menu.add_option("delete user", delete_user)

blog_actions_menu = Menu()

main_menu = Menu()

main_menu.add_option("user actions", user_actions_menu.show)
main_menu.add_option("blog actions", lambda x: x)

main_menu.show()
