from evennia.commands.command import Command as BaseCommand
from evennia.utils.evmenu import EvMenu


def node_choose_name(caller, raw_input, **kwargs):
    text = ""
    options = {"key": "_default",
               "goto": "node_show_hometowns"}

    caller.msg(html="""
            <br>What is the name of the new soul?
            <div>
                <input id="newcharname" class="inputfield form-control" type="text">
                <span onclick="console.log('hi');plugin_handler.onSend(document.getElementById('newcharname').value)">Submit</span>
            </div>
            """, options={"clear": True})

    return text, options


def node_show_hometowns(caller, raw_input, **kwargs):
    text = "From the cosmic void, you see three visions aglow, Each calling out to you, with its tale to bestow."

    name = raw_input.strip()
    # Validate name and send back to name generation node.  Update name generation node to
    # be dynamic depending on if it has an existing name that needs fixing or not

    caller.msg(html="", options={"clear": True})
    options = (
        {"key": "Ashenholme",
         "desc": """A town besieged by dark forces, cries out in despair,
                    Its people plagued by sickness, poverty, and warfare.
                    Their once-thriving home now reduced to rubble and decay,
                    They plead for a hero to rise and show them the way.\n""",
         "goto": ("_create_new_char_in_hometown", {"hometown": "ashenholme", "name": name})},
        {"key": "Verdantus",
         "desc": """An abode nestled in a once-lush forest serene,
                    Now barren, withered, and lifeless, a stark and desolate scene.
                    A blight has taken hold, and nature's beauty fades away,
                    It calls out for a savior, to heal and restore the land to its former sway.\n""",
         "goto": ("_create_new_char_in_hometown", {"hometown": "verdantus", "name": name})},
        {"key": "Aurelia",
         "desc": """A temple of scholars, with knowledge as its treasure,
                    A place of learning, wisdom, and intellectual pleasure.
                    Its secrets and mysteries beckon you to explore,
                    To unravel its truths, and unlock knowledge's door.\n""",
         "goto": ("_create_new_char_in_hometown", {"hometown": "aurelia", "name": name})},
    )

    return text, options


def _create_new_char_in_hometown(caller, raw_input, **kwargs):
    hometown = kwargs.get("hometown")
    name = kwargs.get("name")

    if hometown == 'ashenholme':
        caller.msg("dreams of sanity")

    caller.msg(f"You chose {hometown} with the name of {name}")
    return "node_end"


def node_end(caller, raw_input, **kwargs):
    text = "This da end!"
    return text, None


class CmdCharGen(BaseCommand):
    key = "chargen"
    locks = "cmd:pperm(Player)"

    def func(self):

        menu_nodes = {
            "node_choose_name": node_choose_name,
            "node_show_hometowns": node_show_hometowns,
            "_create_new_char_in_hometown": _create_new_char_in_hometown,
            "node_end": node_end,
        }

        EvMenu(self.caller, menu_nodes, startnode="node_choose_name")
