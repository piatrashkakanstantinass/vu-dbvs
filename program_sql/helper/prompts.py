from prompt_toolkit.document import Document
import questionary


def select(prompt, options):
    if len(options) == 0:
        print("Nothing to select")
        return None
    return questionary.select(prompt, options).unsafe_ask()


def inputMandatory(prompt, default=""):
    res = None
    while res == None:
        res = questionary.text(prompt, default=default).unsafe_ask().strip()
        if len(res) == 0:
            res = None
    return res


def inputOptional(prompt, default=""):
    res = questionary.text(prompt, default=default).unsafe_ask().strip()
    if len(res) == 0:
        res = None
    return res


def inputUsername(default=""):
    return questionary.text(
        "Pick username:", validate=UsernameValidator, default=default
    ).unsafe_ask()


class UsernameValidator(questionary.Validator):
    def validate(self, document):
        if len(document.text) < 5:
            raise questionary.ValidationError(
                message="Username must be at least 5 symbols",
                cursor_position=len(document.text),
            )
