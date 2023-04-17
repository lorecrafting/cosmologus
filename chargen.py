# in mygame/evadventure/chargen.py
from evennia import EvMenu

def start_chargen(caller, session=None):
    """
    This is a start point for spinning up the chargen from a command later.

    """

    menutree = {}  # TODO!

    # this generates all random components of the character
    tmp_character =

    EvMenu(caller, menutree, session=session, tmp_character=tmp_character)
