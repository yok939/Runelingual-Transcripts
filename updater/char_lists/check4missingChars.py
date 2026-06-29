import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def read_second_column_from_tsv(filepath):
    """
    Reads a TSV file and returns the content of the second column.

    :param filepath: The path to the TSV file.
    :return: A list of strings containing the content of the second column.
    """
    second_column_content = ""
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            columns = line.strip().split('\t')
            if len(columns) > 1:
                second_column_content += columns[1]
    return second_column_content

def get_unique_characters(text):
    return set(text)

def get_missing_chars_in_file(files_to_check, reference_file):
    reference_text = read_file(reference_file)
    reference_chars = get_unique_characters(reference_text)

    missing_chars = set()
    for file in files_to_check:
        text = read_second_column_from_tsv(file)
        file_chars = get_unique_characters(text)
        missing_chars.update(file_chars - reference_chars)

    return missing_chars

def get_files_with_extension(directory, extension):
    """
    Fetches all files in the specified directory that end with the specified extension.

    :param directory: The directory to search in.
    :param extension: The file extension to look for.
    :return: A list of file paths that match the specified extension.
    """
    files = []
    print(f"Searching in directory: {directory} for files with extension: {extension}")
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extension):
                file_path = os.path.join(root, filename)
                print(f"Found file: {file_path}")
                files.append(file_path)
    print(f"Total files found: {len(files)}")
    return files

def main():
    extension = ".tsv"
    print("this script will check for missing characters in 'all_char_??.txt' file that exists in files ending with '.tsv' in the specified directory.")

    # choose language
    print("enter a number;")
    LANG = ["ja", "zh_tw"]
    for i, lang in enumerate(LANG):
        print(f"{i} for {lang}")
    language_num = int(input("for the language you wish to check if all character are present in the reference file (all_char_??.txt): "))
    language = LANG[language_num]

    current_file_path = os.path.abspath(__file__)
    target_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_file_path))), "draft")
    target_dir = os.path.join(target_dir, language)
    files = get_files_with_extension(target_dir, extension)
    reference_file = os.path.join(os.path.dirname(current_file_path),"all_char_" + language + ".txt")

    missing_chars = get_missing_chars_in_file(files, reference_file)

    accepted_characters = set("ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ０１２３４５６７８９！？、。\！”＃＄％＆＇（）＊＋，－．／：；＜＝＞？＠［＼］＾＿｀｛｜｝　")
    missing_chars = missing_chars - accepted_characters
    if missing_chars:
        _temp = 0
        print("Characters not found in the reference file:")
        for char in missing_chars:
            print(char, end='')
            _temp += 1
            if _temp % 15 == 0:
                print('\n', end='')
            else:
                if _temp == len(missing_chars):
                    print('\n', end='')
    else:
        print("All characters are present in the reference file.")

if __name__ == "__main__":

    main()
