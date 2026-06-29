import os
import json
import sqlite3
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.append(os.path.join(script_dir, '.'))
# from update_english_transcript import common
import common
    
def connect_to_db(db_file):
    conn = sqlite3.connect(db_file)
    return conn, conn.cursor()

def create_table(cursor):
    """Create the transcript table if it doesn't exist."""
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS transcript (
            key INTEGER PRIMARY KEY, 
            {common.COLUMN_NAME_ENGLISH} TEXT,
            {common.COLUMN_NAME_TRANSLATION} TEXT,
            {common.COLUMN_NAME_CATEGORY} TEXT,
            {common.COLUMN_NAME_SUB_CATEGORY} TEXT,
            {common.COLUMN_NAME_SOURCE} TEXT,
            {common.COLUMN_NAME_WIDGET_ID} INTEGER,
            {common.COLUMN_NAME_PARENT_WIDGET_ID} INTEGER,
            {common.COLUMN_NAME_WIDTH} INTEGER,
            {common.COLUMN_NAME_HEIGHT} INTEGER,
            {common.COLUMN_NAME_NOTES} TEXT,
            {common.COLUMN_NAME_DATE_MODIFIED} TEXT,
            {common.COLUMN_NAME_WIKI_URL} TEXT
        )
    ''')

    cursor.execute(f'''
                   CREATE INDEX IF NOT EXISTS english_index ON transcript ({common.COLUMN_NAME_ENGLISH});
                   ''')

def check_record_exists(c, conditions):
    """
    args:
        c: sqlite3.Cursor object
        conditions: dictionary of column-value pairs to check for existence
    return:
    true if record with same conditions exists, false otherwise
    """
    #base query
    query = f"SELECT 1 FROM {common.TABLE_NAME} WHERE "

    # Dynamically build the WHERE clause based on conditions
    where_clauses = []
    values = []
    for column, value in conditions.items():
        where_clauses.append(f"{column} = ?")
        values.append(value)
    
    # Join all WHERE clauses with 'AND'
    query += " AND ".join(where_clauses)
    # Execute the query
    c.execute(query, tuple(values))
    # Retrieve the result
    result = c.fetchone()
    
    # Check if any record exists based on the stored result
    return result is not None

def insert_cache_json_data(conn, c, data):

    """
    Insert data in the transcript table.
    Args:
        conn: sqlite3.Connection object
        c: sqlite3.Cursor object
        entity_list_of_category: entity list for one of the categories (items, npcs, objects)
        e.g of entity_list_of_category:
            ["item":[{
            "name":"Dwarf remains",
            "examine":"The body of a Dwarf savaged by Goblins.",
            "inventoryActions":[null,null,null,null,"Destroy"]
            },{
            "name":"Toolkit",
            "examine":"Good for repairing broken cannons.",
            "inventoryActions":[null,null,null,null,"Destroy"]
            }
            ],
            "npc":[{
            "name":"Dwarf",
            "examine":"He looks like he's been working hard.",
            "actions":["Talk-to","Trade","Pickpocket"]
            },{...}],
            "object":[{
            "name":"Anvil",
            "examine":"Used for smithing metal items.",
            "actions":["Smith","Craft","Repair"]
            },{...}]
            ]
    """
    for category_type, entity_list_of_category in data.items(): #category_type = "item", "npc", "object"
        for entity in entity_list_of_category: #entity is a dictionary, of either item, npc, or object
            #source_name is the name of the entity 
            source_name = 'unknown'
            if category_type == common.ITEM_KEY:
                source_name = entity[common.ITEM_NAME_VAR_NAME]
            elif category_type == common.NPC_KEY:
                source_name = entity[common.NPC_NAME_VAR_NAME]
            elif category_type == common.OBJECT_KEY:
                source_name = entity[common.OBJECT_NAME_VAR_NAME]

            for key, value in entity.items(): #key = "name", "examine", "inventoryActions" etc
                query = f'''
                        INSERT INTO {common.TABLE_NAME} (
                        {common.COLUMN_NAME_ENGLISH}, 
                        {common.COLUMN_NAME_CATEGORY}, 
                        {common.COLUMN_NAME_SUB_CATEGORY}, 
                        {common.COLUMN_NAME_SOURCE}, 
                        {common.COLUMN_NAME_WIDGET_ID}, 
                        {common.COLUMN_NAME_PARENT_WIDGET_ID}, 
                        {common.COLUMN_NAME_WIDTH}, 
                        {common.COLUMN_NAME_HEIGHT}, 
                        {common.COLUMN_NAME_NOTES}, 
                        {common.COLUMN_NAME_DATE_MODIFIED},
                        {common.COLUMN_NAME_WIKI_URL})
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                # if its a name
                if key in [common.ITEM_NAME_VAR_NAME, common.NPC_NAME_VAR_NAME, common.OBJECT_NAME_VAR_NAME]\
                        and not check_record_exists(c, {common.COLUMN_NAME_ENGLISH:value}):
                    c.execute(query, (value, key, category_type, '', 0, 0, 0, 0, '', common.TODAYS_DATE, ''))

                # if its an examine
                elif key in [common.ITEM_EXAMINE_VAR_NAME, common.NPC_EXAMINE_VAR_NAME, common.OBJECT_EXAMINE_VAR_NAME]\
                        and not check_record_exists(c, {common.COLUMN_NAME_ENGLISH:value}):
                    c.execute(query, (value, key, category_type, source_name, 0, 0, 0, 0, '', common.TODAYS_DATE, ''))


                # if its an option
                elif key in [common.ITEM_OPTION_VAR_NAME, common.NPC_OPTION_VAR_NAME, common.OBJECT_OPTION_VAR_NAME]:
                    for option in value:
                        if type(option) != str or option == "Null":
                            continue
                        elif not check_record_exists(c, {common.COLUMN_NAME_ENGLISH:option, common.COLUMN_NAME_SUB_CATEGORY:category_type}):
                            c.execute(query, (option, key, category_type, source_name, 0, 0, 0, 0, '', common.TODAYS_DATE, ''))
    
    conn.commit()
                        

def jsonFileToSQL(jsonFile):
    with open(jsonFile) as json_file:
        data = json.load(json_file)

    conn, c = connect_to_db(common.DATABASE_PATH)

    #create_table if it doesn't exist
    create_table(c)

    #insert data into the table
    insert_cache_json_data(conn, c, data)
    
def insert_record(c, record):
    """
    args:
    conn: sqlite3.Connection object
    c: sqlite3.Cursor object
    record: dictionary of column-value pairs to insert e.g. {"english": dialogue, "category": category, ...}
    record doesnt contain every column, only the ones that are not empty values
    """
    columns = ', '.join(record.keys())
    val_placeholders = ', '.join(['?' for _ in record.keys()])
    query = f'''
            INSERT INTO {common.TABLE_NAME} (
            {columns})
            VALUES ({val_placeholders})
        '''
    c.execute(query, tuple(record.values()))

def dictListToSQL(dict_data, 
                  skip_if_same_value_in_column = [common.COLUMN_NAME_ENGLISH, common.COLUMN_NAME_CATEGORY,
                                                common.COLUMN_NAME_SUB_CATEGORY, common.COLUMN_NAME_SOURCE],
                                                database_path = common.DATABASE_PATH):
    """
    inserts given data to transcript table
    args:
    dict_data: dictionary in list format: [{"english": dialogue, "category": category, ...}, {...}, ...]
    
    skip_if_same_value_in_column: list of column names to check if the record already exists in the table
                                will only store if no records matches all values in the stated column
    """
    for dict in dict_data: # todo: test this
        for key, value in dict.items():
            if value is not None:
                value = replace_special_spaces(value)
        

    conn, c = connect_to_db(database_path)

    #create_table if it doesn't exist
    create_table(c)

    #insert data into the table
    for record in dict_data:
        if check_record_exists(c, {column: record[column] for column in skip_if_same_value_in_column}):
            continue
        insert_record(c, record)
    conn.commit()
    

def addAllTSVToSQL(TSVDir):
    conn, c = connect_to_db(common.DATABASE_PATH)
    create_table(c)
    
    # iterate through all csv files in the directory
    for root, dirs, files in os.walk(TSVDir):
        for file in files:
            added_records = 0
            # open each files
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:

                for i,line in enumerate(f):
                    line = replace_special_spaces(line)
                    if line.strip() in ['', None, '\n']: # skip empty lines
                        continue
                    line = line.replace('\n','').split('\t')
                    if i == 0: # the first line is the column names
                        column_names = line
                    else: # the rest of the lines are records
                        record = {key : value for key, value in zip(column_names, line)}
                        record.update({common.COLUMN_NAME_DATE_MODIFIED:common.TODAYS_DATE})
                        if not check_record_exists(c, {common.COLUMN_NAME_ENGLISH:record[common.COLUMN_NAME_ENGLISH],
                                                        common.COLUMN_NAME_CATEGORY:record[common.COLUMN_NAME_CATEGORY],
                                                        common.COLUMN_NAME_SUB_CATEGORY:record[common.COLUMN_NAME_SUB_CATEGORY],
                                                        common.COLUMN_NAME_SOURCE:record[common.COLUMN_NAME_SOURCE]}):
                            added_records += 1
                            insert_record(c, record)
            print("Added", added_records, "records from file: " + file)

    conn.commit()
    print("Added all manually created CSV files to SQL")

def replace_special_spaces(input_str):
    if input_str is None:
        return None

    special_spaces = [32, 160, 8195, 8194, 8201, 8202, 8203, 12288]
    result = []

    for char in input_str:
        code_point = ord(char)
        if code_point in special_spaces:
            result.append(' ')
        else:
            result.append(char)

    return ''.join(result)

#for testing
def print_char_ids(input_str):
    for char in input_str:
        print(f"Character: {char}, ID: {ord(char)}")

if __name__ == "__main__":
    #jsonFileToSQL(common.CACHE_UPDATED_PATH)
    #addAllTSVToSQL(common.MANUAL_FILE_DIR)
    original = "Senntisten Teleport"
    replaced = replace_special_spaces(original) # should return "hello world"
    print(original == replaced)
    print(original + ":")
    print_char_ids(original)

    print(replaced + ":")
    print_char_ids(replaced)
