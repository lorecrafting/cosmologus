from django.conf import settings
from evennia import search_object
from evennia.commands.command import Command as BaseCommand
from evennia.utils import class_from_module
from evennia.utils.evmenu import EvMenu
from evennia.objects.models import ObjectDB


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
    new_character = _create_character(caller, key=name)
    print(new_character)
    caller.msg(new_character)

    if hometown == 'ashenholme':
        caller.msg("dreams of ashenholme")
    elif hometown == 'verdantus':
        caller.msg("dreams of verdantus")
    elif hometown == 'aurelia':
        caller.msg("dreams of aurelia")

    caller.msg(
        f"Let it be known that a new soul by the name of {name} has been incarnated into {hometown}!")

    return "node_end"


def _create_character(self, *args, **kwargs):
    """
    Create a character linked to this account.

    Args:
        key (str, optional): If not given, use the same name as the account.
        typeclass (str, optional): Typeclass to use for this character. If
            not given, use settings.BASE_CHARACTER_TYPECLASS.
        permissions (list, optional): If not given, use the account's permissions.
        ip (str, optional): The client IP creating this character. Will fall back to the
            one stored for the account if not given.
        kwargs (any): Other kwargs will be used in the create_call.
    Returns:
        Object: A new character of the `character_typeclass` type. None on an error.
        list or None: A list of errors, or None.

    """
    # parse inputs
    character_key = kwargs.pop("key", self.key)
    character_ip = kwargs.pop("ip", self.db.creator_ip)
    character_permissions = kwargs.pop("permissions", self.permissions)

    # Load the appropriate Character class
    character_typeclass = kwargs.pop("typeclass", None)
    character_typeclass = (
        character_typeclass if character_typeclass else settings.BASE_CHARACTER_TYPECLASS
    )
    Character = class_from_module(character_typeclass)

    if "location" not in kwargs:
        kwargs["location"] = ObjectDB.objects.get_id(settings.START_LOCATION)

    # Create the character
    character, errs = Character.create(
        character_key,
        self,
        ip=character_ip,
        typeclass=character_typeclass,
        permissions=character_permissions,
        **kwargs,
    )
    if character:
        # Update playable character list
        if character not in self.characters:
            self.db._playable_characters.append(character)

        # We need to set this to have @ic auto-connect to this character
        self.db._last_puppet = character
    return character, errs


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
