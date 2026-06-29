from datetime import datetime
import os, send2trash

TODAYS_DATE = datetime.today().strftime('%Y-%m-%d')

# Absolute path of the current file
current_file_path = os.path.abspath(__file__)
# Absolute path of the folder containing the current file
current_folder_path = os.path.dirname(current_file_path)
parent_folder_path = os.path.dirname(current_folder_path)

DATABASE_PATH = os.path.join(parent_folder_path,"transcript.db")
MANUAL_FILE_DIR = os.path.join(current_folder_path,"manual_data/")

TABLE_NAME = "transcript"

# KEYs are the values in column
ITEM_KEY = "item"
NPC_KEY = "npc"
OBJECT_KEY = "object"

# VAR_NAMEs are static values inserted to the database
ITEM_NAME_VAR_NAME = "name"
NPC_NAME_VAR_NAME = "name"
OBJECT_NAME_VAR_NAME = "name"

ITEM_EXAMINE_VAR_NAME = "examine"
NPC_EXAMINE_VAR_NAME = "examine"
OBJECT_EXAMINE_VAR_NAME = "examine"

ITEM_OPTION_VAR_NAME = "inventoryActions"
NPC_OPTION_VAR_NAME = "actions"
OBJECT_OPTION_VAR_NAME = "actions"
ITEM_GROUND_OPTION_VAR_NAME = "actions"

NPC_DIALOGUE_VAR_NAME = "dialogue"
LEVEL_UP_VAR_NAME = "lvl_up_msg"

#COLUMN_NAMEs are the column names in the database
COLUMN_NAME_ENGLISH = "english"
COLUMN_NAME_TRANSLATION = "translation"
COLUMN_NAME_CATEGORY = "category"
COLUMN_NAME_SUB_CATEGORY = "sub_category"
COLUMN_NAME_SOURCE = "source"
COLUMN_NAME_WIDGET_ID = "widget_id"
COLUMN_NAME_PARENT_WIDGET_ID = "parent_widget_id"
COLUMN_NAME_WIDTH = "width"
COLUMN_NAME_HEIGHT = "height"
COLUMN_NAME_NOTES = "notes"
COLUMN_NAME_DATE_MODIFIED = "date_modified"
COLUMN_NAME_WIKI_URL = "wiki_url"

WIKI_URL = {"npc_dialogue" : "https://oldschool.runescape.wiki/w/Category:NPC_dialogue",
            "pet_dialogue" : "https://oldschool.runescape.wiki/w/Category:Pet_dialogue",
            "level_up_message" : "https://oldschool.runescape.wiki/w/Category:Level_up_messages",
            "examine" : "https://oldschool.runescape.wiki/w/",
            "base" : "https://oldschool.runescape.wiki"}
FETCH_NPCDIALOGUE = True
FETCH_PETDIALOGUE = True
FETCH_LEVELUPMESSAGE = True
FETCH_EXAMINE = True
FETCH_ITEM_NPC_OBJECT_URLS = False

CHISEL_URL = {"item_main" : "https://chisel.weirdgloop.org/moid/data_files/itemsmin.js",
              "npc_main" : "https://chisel.weirdgloop.org/moid/data_files/npcsmin.js",
              "object_main" : "https://chisel.weirdgloop.org/moid/data_files/objectsmin.js",
              "npc_examine": "https://chisel.weirdgloop.org/moid/data_files/npc_examinesmin.js",
              "object_examine": "https://chisel.weirdgloop.org/moid/data_files/object_examinesmin.js",}


# DONT CHANGE unless the chisel data changes
CHISEL_CATEGORY_NAME = {'item' : 'items', 'npc' : 'npcs', 'object' : 'objects', 'name': 'name',\
                        'examine' : 'examine', 'action_item' : 'actInv',\
                        'action_npc' : 'actions', 'action_object' : 'actions'}

WIKI_SEARCH_BASE_URL = {"npc" : "https://oldschool.runescape.wiki/?title=Special%3ASearchByProperty&property=NPC+ID&value=",
                        "object" : "https://oldschool.runescape.wiki/?title=Special%3ASearchByProperty&property=Object+ID&value=",
                        "item" : "https://oldschool.runescape.wiki/?title=Special%3ASearchByProperty&property=Item+ID&value="}


NAME_SUB_CATEGORY = ['item', 'npc', 'object', 'menu', 'level'] # (todo: add here when adding new sub categories to category=name) the sub categories that exist where category(column) = name 
SUB_CAT_WITH_NO_EXAMINE = ['menu', 'level'] # todo: add sub categories that do not have an examine column
def delete_file(file_path):
    if os.path.exists(file_path):
        send2trash.send2trash(file_path)
        print(f"File {file_path} has been moved to recycle bin.")
    else:
        print(f"File not found: {file_path}")
