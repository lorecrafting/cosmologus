# in mygame/evadventure/chargen.py
from evennia import EvMenu

def _handle_answer(caller, raw_input, **kwargs):
    answer = kwargs.get("answer")
    caller.msg(f"You chose {answer}!")
    return "end"  # name of next node

menu_template = """

## node start

Is your answer yes or no?

## options

[Y]es!;yes;y: Answer yes. -> handle_answer(answer=yes)
[N]o!;no;n: Answer no. -> handle_answer(answer=no)
[A]bort;abort;a: Answer neither, and abort. -> end

## node end

Thanks for your answer. Goodbye!

"""
