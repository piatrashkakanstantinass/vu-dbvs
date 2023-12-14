"""
post actions
selct which post

comments
  list comments
  create comment (get username)
  update comment
  delete comment

"""
from tabulate import tabulate

from .helper.menu import Menu
from .helper import prompts, db

from .entities.user import User
from .entities.blog import Blog
from .entities.post import Post
from .entities.comment import Comment


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


def create_comment(post_id):
    comment = comment_prompt(ask_for_user=True)
    comment.post_id = post_id
    Comment.create(comment)


def update_comment(post_id):
    comment = pick_comment(post_id)
    if comment == None:
        return
    new_comment = comment_prompt(comment)
    new_comment.comment_id = comment.comment_id
    Comment.update(new_comment)


def delete_comment(post_id):
    comment = pick_comment(post_id)
    if comment == None:
        return
    Comment.delete(comment.comment_id)


def comment_prompt(comment=None, ask_for_user=False):
    user = None
    if ask_for_user:
        print("Who's commenting?")
        user = pick_user()
    content = prompts.inputMandatory("Comment", getattr(comment, "content", ""))
    return Comment(
        0, content, getattr(user, "user_id", 0), 0, getattr(user, "username", ""), 0
    )


def pick_comment(post_id):
    comments = Comment.get(post_id)
    comment_contents = [comment.content for comment in comments]
    content = prompts.select("Pick comment", comment_contents)
    if content == None:
        return
    for comment in comments:
        if comment.content == content:
            return comment


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


def go_to_post_actions(blog_id):
    post = pick_post(blog_id)
    if post == None:
        return
    post_view_actions_menu.show(post.post_id)


def show_user_stats(state):
    with db.get_cursor() as cursor:
        cursor.execute("REFRESH MATERIALIZED VIEW UsersStats")
        cursor.execute(
            "SELECT username, blog_count, post_count, received_comment_count FROM UsersStats"
        )
        entries = cursor.fetchall()
        cursor.connection.commit()
    print(
        tabulate(
            entries, ["Username", "Blog count", "Post count", "Received comment count"]
        )
    )


user_actions_menu = Menu()
user_actions_menu.add_option("list users", lambda s: print(User.get_table(User.get())))
user_actions_menu.add_option("create user", create_user)
user_actions_menu.add_option("update user", update_user)
user_actions_menu.add_option("delete user", delete_user)
user_actions_menu.add_option("show user stats", show_user_stats)

post_view_actions_menu = Menu()
post_view_actions_menu.add_option(
    "list comments", lambda s: print(Comment.get_table(Comment.get(s)))
)
post_view_actions_menu.add_option("post comment", create_comment)
post_view_actions_menu.add_option("update comment", update_comment)
post_view_actions_menu.add_option("delete comment", delete_comment)


post_actions_menu = Menu()
post_actions_menu.add_option("list posts", lambda s: print(Post.get_table(Post.get(s))))
post_actions_menu.add_option("create post", create_post)
post_actions_menu.add_option("update post", update_post)
post_actions_menu.add_option("delete post", delete_post)
post_actions_menu.add_option("view post (comment section)", go_to_post_actions)

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
