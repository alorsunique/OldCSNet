# This code should change the author field, merging the needed info to be merged
# This code should also copy selected data from the Scopus file to another CSV for faster processing
# A final complete list should also be generated


import os
import sys

from pathlib import Path

script_path = Path(__file__).resolve()
project_dir = script_path.parent.parent
os.chdir(project_dir)
sys.path.append(str(project_dir))

import shutil
import csv

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

max_int = sys.maxsize

while True:
    # Decrease the maxInt value by factor 10
    # As long as the OverflowError occurs.

    try:
        csv.field_size_limit(max_int)
        break
    except OverflowError:
        max_int = int(max_int / 10)

project_dir = os.getcwd()

scopus_dir = os.path.join(project_dir, "Scopus Files")
prelim_extract_dir = os.path.join(project_dir, "Preliminary Extracted Info")

# Makes the necessary folders
if not os.path.exists(scopus_dir):
    os.mkdir(scopus_dir)

if os.path.exists(prelim_extract_dir):
    shutil.rmtree(prelim_extract_dir)  # Clears the extracted folder
os.mkdir(prelim_extract_dir)

suffix_merge_term = ["jr", "jr.", "ii", "iii", "iv", "v"]  # Terms that will be merged to the previous entry

# Creates global database

for file in os.listdir(scopus_dir):

    print(file)

    # Here the CSV file is read and contents are taken

    source_file = os.path.join(scopus_dir, file)

    cur_file = open(source_file, encoding="UTF-8")  # Current file being read
    file_reader = csv.reader(cur_file)

    rows = []
    for row in file_reader:
        rows.append(row)

    cur_file.close()

    # Prepares the institute CSV file

    filename = os.path.splitext(file)[0].replace('Scopus', '')
    filename = filename.strip()
    filename = f"{filename} Extract.csv"

    filepath = os.path.join(prelim_extract_dir, filename)

    # Creates the CSV object
    creator = open(filepath, "x", encoding="UTF-8")
    creator.close()

    # Indexes of info to be taken

    authors_index = rows[0].index('\ufeffAuthors')
    title_index = rows[0].index('Title')
    year_index = rows[0].index('Year')
    author_affi_index = rows[0].index('Authors with affiliations')

    count = 1

    institute_object = open(filepath, "a", encoding='UTF-8', newline='')
    institute_writer = csv.writer(institute_object, delimiter=",")

    # In here the author names are processed and cleaned

    while count < len(rows):

        author_hold = rows[count][authors_index].split(",")

        pre_clean_list = []

        for author in author_hold:
            author = author.strip()
            author = author.lower()
            pre_clean_list.append(author)

        name_count = 0

        clean_list = []

        while name_count < len(pre_clean_list):
            try:
                if pre_clean_list[name_count + 1] in suffix_merge_term:
                    if pre_clean_list[name_count + 1] == "jr.":
                        name_append = f"{pre_clean_list[name_count]} jr"
                    else:
                        name_append = f"{pre_clean_list[name_count]} {pre_clean_list[name_count + 1]}"
                    name_count += 2

                    clean_list.append(name_append)
                else:
                    name_append = pre_clean_list[name_count]

                    name_count += 1

                    clean_list.append(name_append)
            except:
                if pre_clean_list[name_count] not in suffix_merge_term:
                    name_append = pre_clean_list[name_count]
                    name_count += 1

                    clean_list.append(name_append)

        title = rows[count][title_index]
        institute = os.path.splitext(file)[0].replace('Scopus', '')
        institute = institute.strip()
        affiliation = rows[count][author_affi_index]

        # Creates the info pack to be written

        info_pack = []

        info_pack.append(clean_list)
        info_pack.append(title)
        info_pack.append(rows[count][year_index])
        info_pack.append(institute)
        info_pack.append(affiliation)

        institute_writer.writerow(info_pack)

        count += 1

    institute_object.close()
