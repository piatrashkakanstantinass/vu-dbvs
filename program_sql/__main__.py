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
from .entities.blog import Blog
from .entities.post import Post


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
    username = prompts.inputUsername(getattr(user, "username", ""))
    email = prompts.inputMandatory("Pick email", getattr(user, "email", ""))
    first_name = prompts.inputOptional(
        "Pick first name", getattr(user, "first_name", "")
    )
    last_name = prompts.inputOptional("Pck last name", getattr(user, "last_name", ""))
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


def create_blog(user_id):
    blog = blog_prompt()
    blog.user_id = user_id
    Blog.create(blog)


def update_blog(user_id):
    blog = pick_blog(user_id)
    if blog == None:
        return
    new_blog = blog_prompt(blog)
    new_blog.blog_id = blog.blog_id
    Blog.update(new_blog)


def delete_blog(user_id):
    blog = pick_blog(user_id)
    if blog == None:
        return
    Blog.delete(blog.blog_id)


def blog_prompt(blog=None):
    blog_name = prompts.inputMandatory("Pick name", getattr(blog, "blog_name", ""))
    blog_description = prompts.inputOptional(
        "Pick description", getattr(blog, "blog_description", "")
    )
    blog_status = "OPEN"
    if blog != None:
        blog_status = prompts.select("Pick status", ["OPEN", "CLOSED", "HIDDEN"])
    return Blog(0, blog_name, 0, "", blog_status, blog_description)


def pick_blog(user_id):
    blogs = Blog.get(user_id)
    blog_names = [blog.blog_name for blog in blogs]
    blog_name = prompts.select("Pick blog", blog_names)
    if blog_name == None:
        return
    for blog in blogs:
        if blog.blog_name == blog_name:
            return blog


def create_post(blog_id):
    post = post_prompt()
    post.blog_id = blog_id
    Post.create(post)


def update_post(blog_id):
    post = pick_post(blog_id)
    if post == None:
        return
    new_post = post_prompt(post)
    new_post.post_id = post.post_id
    Post.update(new_post)


def delete_post(blog_id):
    post = pick_post(blog_id)
    if post == None:
        return
    Post.delete(post.post_id)


def post_prompt(post=None):
    title = prompts.inputMandatory("Pick title", getattr(post, "title", ""))
    content = prompts.inputOptional("Content", getattr(post, "content", ""))
    return Post(0, title, content, 0, 0, 0, 0)


def pick_post(blog_id):
    posts = Post.get(blog_id)
    post_titles = [post.title for post in posts]
    title = prompts.select("Pick post", post_titles)
    if title == None:
        return
    for post in posts:
        if post.title == title:
            return post


def go_to_blogs(state):
    user = pick_user()
    if user == None:
        return
    blog_actions_menu.show(user.user_id)


def go_to_posts(user_id):
    blog = pick_blog(user_id)
    if blog == None:
        return
    post_actions_menu.show(blog.blog_id)


user_actions_menu = Menu()
user_actions_menu.add_option("list users", lambda s: print(User.get_table(User.get())))
user_actions_menu.add_option("create user", create_user)
user_actions_menu.add_option("update user", update_user)
user_actions_menu.add_option("delete user", delete_user)


post_actions_menu = Menu()
post_actions_menu.add_option("list posts", lambda s: print(Post.get_table(Post.get(s))))
post_actions_menu.add_option("create post", create_post)
post_actions_menu.add_option("update post", update_post)
post_actions_menu.add_option("delete post", delete_post)

blog_actions_menu = Menu()
blog_actions_menu.add_option("list blogs", lambda s: print(Blog.get_table(Blog.get(s))))
blog_actions_menu.add_option("create blog", create_blog)
blog_actions_menu.add_option("update blog", update_blog)
blog_actions_menu.add_option("delete blog", delete_blog)
blog_actions_menu.add_option("go to posts", go_to_posts)

main_menu = Menu()


main_menu.add_option("user actions", user_actions_menu.show)
main_menu.add_option("blog actions", go_to_blogs)

main_menu.show()
