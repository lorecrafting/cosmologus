from evennia.commands.command import Command as BaseCommand
from evennia.utils.evmenu import EvMenu, get_input


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

    caller.msg(html="blap", options={"clear": True})
    options = (
        {"key": "Ashenholme",
         "desc": "ashendesc",
         "goto": (_handle_hometown, {"hometown": "ashenholm"})},
        {"key": "Verdantus",
         "desc": "verdesc.",
         "goto": (_handle_hometown, {"hometown": "verdantus"})},
        {"key": "Aurelia",
         "desc": "aurelia desc",
         "goto": (_handle_hometown, {"hometown": "aurelia"})},
    )

    caller.msg(name)
    # caller.msg(html=f"""
    #     <br><br>
    #     <span onclick="plugin_handler.onSend('ashenholm')"
    #             style="color:white;cursor:pointer"><u></b>Ashenholme</b></u>
    #     </span>, besieged by dark forces, cries out in despair,
    #     Its people plagued by sickness, poverty, and warfare.
    #     Their once-thriving home now reduced to rubble and decay,
    #     They plead for a hero to rise and show them the way.

    #     <br><br>
    #     <span style="cursor:pointer;"
    #             onclick="plugin_handler.onSend('verdantus')"
    #             style="color:white;cursor:pointer"><u></b>Verdantus</b></u>
    #     </span>, nestled in a once-lush forest serene,
    #     Now barren, withered, and lifeless, a stark and desolate scene.
    #     A blight has taken hold, and nature's beauty fades away,
    #     It calls out for a savior, to heal and restore the land to its former sway.

    #     <br><br>
    #     <span onclick="plugin_handler.onSend('aurelia {name}')"
    #             style="color:white;cursor:pointer"><u></b>Aurelia</b></u>
    #     </span>, the temple of scholars, with knowledge as its treasure,
    #     A place of learning, wisdom, and intellectual pleasure.
    #     Its secrets and mysteries beckon you to explore,
    #     To unravel its truths, and unlock knowledge's door.

    #     <br><br>
    #     As you ponder, which vision to heed,
    #     Each vision grows clearer, its call, a potent seed.
    #     Your choice will determine the fate of the land.""")

    return text, options


def _handle_hometown(caller, raw_input, **kwargs):
    hometown = kwargs.get("hometown")
    caller.msg(f"You chose {hometown}")
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
            "node_end": node_end,
        }

        EvMenu(self.caller, menu_nodes, startnode="node_choose_name")
