import jsonHandler, webScraper
import common
import argparse

def add_chisel_data_to_db():
    # fetch from chisel
    item_names, item_examines, item_options \
        = webScraper.scrape_chisel(common.CHISEL_URL["item_main"], common.CHISEL_URL["item_main"])
    npc_names, npc_examines, npc_options \
         = webScraper.scrape_chisel(common.CHISEL_URL["npc_main"], common.CHISEL_URL["npc_examine"])
    object_names, object_examines, object_options \
        = webScraper.scrape_chisel(common.CHISEL_URL["object_main"], common.CHISEL_URL["object_examine"])
    
    for name_data in [item_names, npc_names, object_names]:
        jsonHandler.dictListToSQL(name_data, [common.COLUMN_NAME_ENGLISH, common.COLUMN_NAME_CATEGORY, common.COLUMN_NAME_SUB_CATEGORY])
    for examine_data in [item_examines, npc_examines, object_examines]:
        jsonHandler.dictListToSQL(examine_data, [common.COLUMN_NAME_ENGLISH, common.COLUMN_NAME_CATEGORY, common.COLUMN_NAME_SUB_CATEGORY])
    for option_data in [item_options, npc_options, object_options]:
        jsonHandler.dictListToSQL(option_data, [common.COLUMN_NAME_ENGLISH, common.COLUMN_NAME_CATEGORY, common.COLUMN_NAME_SUB_CATEGORY])

def add_wiki_data_to_db():
    # fetch from wiki
    wiki_data = webScraper.scrape_wiki()
    jsonHandler.dictListToSQL(wiki_data, [common.COLUMN_NAME_ENGLISH, common.COLUMN_NAME_CATEGORY, 
                                          common.COLUMN_NAME_SUB_CATEGORY, common.COLUMN_NAME_SOURCE])

def main():
    # delete all data in the database
    common.delete_file(common.DATABASE_PATH)

    # fetch from chisel
    add_chisel_data_to_db()


    # fetch from wiki
    add_wiki_data_to_db()
    
    #add manual data
    jsonHandler.addAllTSVToSQL(common.MANUAL_FILE_DIR)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='updates the English transcripts')
    parser.add_argument('--updateAll', action='store_true', help='TAKES TIME. Deletes all English data, downloads all data from chisel and wiki, gets data from the manual files, and create a new database')
    parser.add_argument('--addManual', action='store_true', help='gets data from the manual files and updates the database')
    parser.add_argument('--addChisel', action='store_true', help='gets data from chisel and updates the database')
    parser.add_argument('--addWiki', action='store_true', help='gets data from wiki and updates the database')

    args = parser.parse_args()
    if args.updateAll:
        main()
    elif args.addManual:
        jsonHandler.addAllTSVToSQL(common.MANUAL_FILE_DIR)
    elif args.addChisel:
        add_chisel_data_to_db()
    elif args.addWiki:
        add_wiki_data_to_db()
    else:
        print("Please specify an argument")
        print("--updateAll : To update everything (manual transcripts, chisel data (npc, item, object names + examines + options), wiki data (npc dialogues)): python main_generate_English_transcript.py --updateAll")
        print("--addManual : Does not delete current data, just add manual transcripts")
        print("--addChisel : Does not delete current data, just add chisel data (npc, item, object names + examines + options)")
        print("--addWiki : Does not delete current data, just add wiki data (npc dialogues)")
        exit(1)
