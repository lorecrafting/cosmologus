from evennia.commands.command import Command as BaseCommand
from evennia.utils.evmenu import EvMenu

def _handle_answer(caller, raw_input, **kwargs):
        answer = kwargs.get("answer")
        caller.msg(f"You chose {answer}!")
        return "end"  # name of next node

def node_question(caller, raw_input, **kwargs):
    text = "Is your answer yes or no?"
    options = (
        {"key": ("[Y]es!", "yes", "y"),
         "desc": "Answer yes.",
         "goto": (_handle_answer, {"answer": "yes"})},
        {"key": ("[N]o!", "no", "n"),
         "desc": "Answer no.",
         "goto": (_handle_answer, {"answer": "no"})},
        {"key": ("[A]bort", "abort", "a"),
         "desc": "Answer neither, and abort.",
         "goto": "end"}
    )
    return text, options

def node_end(caller):
    text = "Goodbye!"
    return text, None
class CmdCharGen(BaseCommand):
    key = "chargen"
    locks = "cmd:pperm(Player)"

    def func(self):
        EvMenu(self.caller, {"start": node_question, "end": node_end})
        self.msg('chargenWOOT')
