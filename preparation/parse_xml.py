# coding: utf-8


import xml.etree.ElementTree as ET
import os, fnmatch
from os.path import join
import re
from collections import defaultdict
import configparser

# ### Using XPATH


######################## application-reference_doc-number
def get_app_ref_doc_number():
    for path in root.findall("./bibliographic-data/application-reference/document-id/doc-number"):
        app_ref_doc_num = path.text
    return app_ref_doc_num


######################## classification-ipcr

def get_classification_ipcr():
    classification_text = ""
    label_lookup_key_list = []
    for path in root.findall("./bibliographic-data/technical-data/classifications-ipcr/classification-ipcr"):
        path_text = path.text.strip()
        first_14 = path_text[:14]
        from_15 = path_text[14:].strip()
        first_14_list = first_14.split()

        if (len(first_14_list) == 2):
            first_14 = first_14.replace('/', '').replace(' ', '0')
            first_14 = first_14.ljust(14, '0')
        else:
            first_14 = first_14.strip()
        #         print("path_text,first_14","|"+path_text+"|"+first_14+"|")

        label_lookup_key_list.append(first_14)
        #         classification_text = (classification_text + "|" + (first_14 + "~" + from_15).strip()).strip('|')
        classification_text = (classification_text + "|" + first_14 + "~" + from_15).strip('|')

    return (classification_text, label_lookup_key_list)


t = 'test'
t.ljust(10, '0')


######################## invention-title in English

def get_invention_title():
    inv_title = 'NA'
    for path in root.findall("./bibliographic-data/technical-data/invention-title"):
        lang = path.get("lang")
        if lang == "EN":
            inv_title = path.text
    return inv_title


######################## abstract in English
def get_abstract_text():
    pattern = re.compile("\([0-9]*\)")
    abstract_text = 'NA'
    for path in root.findall("./abstract"):
        lang = path.get("lang")
        if lang == "EN":
            abstract_text = ""
            for child in path.getchildren():
                abstract_text_tmp = child.text
                abstract_text = abstract_text + " " + (abstract_text_tmp or '')
            abstract_text = re.sub(pattern, '', abstract_text)
            abstract_text = re.sub('\s+', ' ', abstract_text.replace('\\n', ' ')).strip()
    return abstract_text


######################## description in English

def get_description_text():
    desc_text = "NA"
    for path in root.findall("./description"):
        lang = path.get("lang")
        if lang == "EN":
            desc_text = ""
            for child in path.getchildren():
                # or is used for replacing None
                desc_text = desc_text + " " + (child.text or '')
            # replacing newlines and multiple spaces
            desc_text = re.sub('\s+', ' ', desc_text.replace('\\n', ' ')).strip()

    return desc_text


######################## claim_text in English

def get_claim_text():
    pattern = re.compile("\([0-9,]*\)")
    # Removing words such as (6,7), (4)

    claim_text = "NA"
    for path in root.findall("./claims"):
        lang = path.get("lang")
        if lang == "EN":
            claim_text = ""
            for child in path.getchildren():
                claim_text_tmp = child.find('claim-text').text
                claim_text = claim_text + " " + (claim_text_tmp or '')
            claim_text = re.sub(pattern, '', claim_text)
            claim_text = re.sub('\s+', ' ', claim_text.replace('\\n', ' ')).strip()
    return claim_text


######################## Final files
def write_files():
    with open(join(outDIR, fileNameToDocNumber), "a+") as f:
        write_str = file_path_new + "|" + app_ref_doc_num
        f.write(write_str + '\n')

    with open(join(outDIR, fileDocNumberToClassText), "a+") as f:
        write_str = app_ref_doc_num + "|" + classification_text
        f.write(write_str + '\n')

    with open(join(outDIR, fileDocNumberToInvTitle), "a+") as f:
        write_str = app_ref_doc_num + "|" + inv_title
        f.write(write_str + '\n')

    with open(join(outDIR, fileDocNumberToAbsText), "a+") as f:
        write_str = app_ref_doc_num + "|" + abstract_text
        f.write(write_str + '\n')

    with open(join(outDIR, fileDocNumberToDescText), "a+") as f:
        write_str = app_ref_doc_num + "|" + desc_text
        f.write(write_str + '\n')

    with open(join(outDIR, fileDocNumberToClaimText), "a+") as f:
        write_str = app_ref_doc_num + "|" + claim_text
        f.write(write_str + '\n')

    with open(join(outDIR, fileDocNumberToLabels), "a+") as f:
        write_str = app_ref_doc_num + "|" + claim_text
        f.write(write_str + '\n')

######################## Read label files and store them in a dictionary

def read_label_files():
    label_dict = {}
    for dName, sdName, fList in os.walk(labelDIR):
        for fileName in fList:
            if fnmatch.fnmatch(fileName, labelPattern):
                file_path = join(dName, fileName)
                with open(file_path, 'r') as fp:
                    line = fp.readline().rstrip('\r\n')
                    while line:
                        (key, value) = re.split(r'\t+', line)
                        label_dict[key] = (fileName, value)
                        line = fp.readline().rstrip('\r\n')
    return label_dict


######################## Get the labels

def get_labels():
    labels_list = []
    for key in label_lookup_key_list:
        labels_list.append(label_dict[key])
    labels_string = "|".join(str(e) for e in labels_list)
    return labels_string

######################## MAIN ########################

config = configparser.ConfigParser()
config.read('../config/config.ini')

inDIR = config['DEFAULT']['inDIR']
pattern = config['DEFAULT']['pattern']
outDIR = config['DEFAULT']['outDIR']
fileNameToDocNumber = config['DEFAULT']['fileNameToDocNumber']
fileDocNumberToClassText = config['DEFAULT']['fileDocNumberToClassText']
fileDocNumberToInvTitle = config['DEFAULT']['fileDocNumberToInvTitle']
fileDocNumberToAbsText = config['DEFAULT']['fileDocNumberToAbsText']
fileDocNumberToDescText = config['DEFAULT']['fileDocNumberToDescText']
fileDocNumberToClaimText = config['DEFAULT']['fileDocNumberToClaimText']
fileDocNumberToLabels = config['DEFAULT']['fileDocNumberToLabels']
labelPattern = config['DEFAULT']['labelPattern']
labelDIR = config['DEFAULT']['labelDIR']
limit_files_write = config.getint('DEFAULT','limit_files_write')
path_string_to_replace = config['DEFAULT']['path_string_to_replace']

fileList = []
doc_number_filename = defaultdict(list)
cnt_files = 0


# Read label files

label_dict = {}
label_dict = read_label_files()
print("Completed label_dict")
pattern_path = re.compile("^"+path_string_to_replace)


for dName, sdName, fList in os.walk(inDIR):
    outer_break_flag = 0
    for fileName in fList:
        # Match search pattern
        if fnmatch.fnmatch(fileName, pattern):
            cnt_files = cnt_files + 1
            
            # Controls the number of files read
            if cnt_files == limit_files_write:
                outer_break_flag = 1
                break

            file_path = join(dName, fileName)
            file_path_new = re.sub(pattern_path, '', file_path)

            tree = ET.parse(file_path)
            root = tree.getroot()
            app_ref_doc_num = get_app_ref_doc_number()

            label_lookup_key_list = []
            (classification_text, label_lookup_key_list) = get_classification_ipcr()
            labels = get_labels()
            inv_title = get_invention_title()
            abstract_text = get_abstract_text()
            desc_text = get_description_text()
            claim_text = get_claim_text()

            write_files()

    if outer_break_flag == 1:
        break





