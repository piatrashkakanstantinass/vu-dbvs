"""
Menu

register callable
"""

# main_menu = Menu()

# user_actions_menu = Menu()
# blog_actions_menu = Menu() # pick user
import psycopg2
from . import prompts


class Menu:
    options = []
    state = None

    EXIT_OPTION = "back"

    def __init__(self, state=None):
        self.options = []
        self.state = state

    def add_option(self, label, callback):
        self.options.append((label, callback))

    def show(self, state=None):
        if state == None:
            state = self.state
        while True:
            try:
                labels = [label for (label, callback) in self.options] + [
                    self.EXIT_OPTION
                ]
                selected_label = prompts.select("Pick option", labels)
                if selected_label == self.EXIT_OPTION:
                    break
                for opt_label, callback in self.options:
                    if opt_label == selected_label:
                        try:
                            callback(state)
                        except KeyboardInterrupt:
                            continue

            except psycopg2.errors.UniqueViolation:
                print("Entry already exists")
            except KeyboardInterrupt:
                break
