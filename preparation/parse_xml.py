# coding: utf-8


import configparser
import datetime
import fnmatch
import gzip
import os
import re
import shutil
import xml.etree.ElementTree as ET
from collections import defaultdict
from os.path import join


# ### Using XPATH


######################## application-reference_doc-number
def get_app_ref_doc_number():
    for path in root.findall("./bibliographic-data/application-reference/document-id/doc-number"):
        app_ref_doc_num = path.text.replace('|', ' ')
    return app_ref_doc_num


######################## application_date
def get_application_date():
    for path in root.findall("./bibliographic-data/application-reference/document-id/date"):
        application_date = path.text
    return application_date


######################## classification-ipcr

def get_classification_ipcr():
    #Not using docNumberToClassText# classification_text = ""
    #Not using labels# label_lookup_key_list = []
    label_sub_class_lookup_key_list = []

    for path in root.findall("./bibliographic-data/technical-data/classifications-ipcr/classification-ipcr"):
        path_text = (path.text or '').replace('|', ' ').strip()
        first_14 = path_text[:14]
        from_15 = path_text[14:].strip()
        first_14_list = first_14.split()
        
        if (len(first_14_list) == 2):
            first_14 = first_14.replace('/', '').replace(' ', '0')
            first_14 = first_14.ljust(14, '0')
        else:
            first_14 = first_14.strip()
        #         print("path_text,first_14","|"+path_text+"|"+first_14+"|")
        
        # first_14 now contains the most granular label padded with zeroes
        
        # label_sub_class such as H01M
        label_sub_class = first_14[0:4]

        #Not using labels# label_lookup_key_list.append(first_14)
        label_sub_class_lookup_key_list.append(label_sub_class)
        
        #Not using docNumberToClassText# classification_text = (classification_text + "|" + first_14 + "~" + from_15).strip('|')
    
    # deduping
    #Not using docNumberToClassText# label_lookup_key_list = list(set(label_lookup_key_list))
    label_sub_class_lookup_key_list = list(set(label_sub_class_lookup_key_list))
    # label_sub_class_lookup_key_string = '|'.join(str(e) for e in label_sub_class_lookup_key_list)
    return label_sub_class_lookup_key_list


######################## invention-title in English

def get_invention_title():
    inv_title = 'NA'
    for path in root.findall("./bibliographic-data/technical-data/invention-title"):
        lang = path.get("lang")
        if lang == "EN":
            inv_title = (path.text or '').replace('|', ' ')
    
    # Truncating to 150 words
    # inv_title = " ".join(inv_title.split()[:limit_word_count])
    
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
                abstract_text_tmp = (child.text or '').replace('|', ' ')
                abstract_text = abstract_text + " " + (abstract_text_tmp or '')
            abstract_text = re.sub(pattern, '', abstract_text)
            abstract_text = re.sub('\s+', ' ', abstract_text.replace('\\n', ' ')).strip()
    
    # Truncating to 150 words
    # abstract_text = " ".join(abstract_text.split()[:limit_word_count])
    
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
                desc_text = desc_text + " " + (child.text or '').replace('|', ' ')
            # replacing newlines and multiple spaces
            desc_text = re.sub('\s+', ' ', desc_text.replace('\\n', ' ')).strip()
    
    # Truncating to 150 words
    # desc_text = " ".join(desc_text.split()[:limit_word_count])
    
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
                claim_text_tmp = (child.find('claim-text').text or '').replace('|', ' ')
                # claim_text = claim_text + " " + (claim_text_tmp or '')
                claim_text = claim_text + " " + claim_text_tmp
            claim_text = re.sub(pattern, '', claim_text)
            claim_text = re.sub('\s+', ' ', claim_text.replace('\\n', ' ')).strip()
    
    # Truncating to 150 words
    # claim_text = " ".join(claim_text.split()[:limit_word_count])
    return claim_text


######################## Final files
def write_files():
    with open(join(outDIR, fileNameToDocNumber), "a+") as f:
        write_str = file_path_new + "|" + app_ref_doc_num
        f.write(write_str + '\n')
    
    # with open(join(outDIR, fileDocNumberToClassText), "a+") as f:
    #     write_str = app_ref_doc_num + "|" + classification_text
    #     f.write(write_str + '\n')
    
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
    
    # with open(join(outDIR, fileDocNumberToLabels), "a+") as f:
    #     write_str = app_ref_doc_num + "|" + labels
    #     f.write(write_str + '\n')

    
    with open(join(outDIR, fileDocNumberToLabelSubClassCode), "a+") as f:
        write_str = app_ref_doc_num + "|" + label_sub_class_lookup_key_string
        f.write(write_str + '\n')

    with open(join(outDIR, fileDocNumberToLabelSubClass), "a+") as f:
        write_str = app_ref_doc_num + "|" + label_sub_class
        f.write(write_str + '\n')


######################## Read label files and store them in a dictionary

def read_label_files():
    label_dict = {}
    for dName, sdName, fList in os.walk(labelDIR):
        for fileName in fList:
            if fnmatch.fnmatch(fileName, labelPattern):
                file_path = join(dName, fileName)
                with open(file_path, 'r') as fp:
                    line = fp.readline().rstrip('\r\n').replace('|', ' ')
                    while line:
                        (key, value) = re.split(r'\t+', line)
                        value = re.sub(label_pattern_to_replace, '', value)
                        label_dict[key] = (fileName, value)
                        line = fp.readline().rstrip('\r\n')
    return label_dict


######################## Get the most granular labels

# def get_labels(l_file_path_new, l_app_ref_doc_num):
#     labels_list = []
#     for key in label_lookup_key_list:
#         if key not in label_dict.keys():
#             # Checks for missing label keys missing in label source and writes them to error files
#             error_message = ("LabelKey:{key}|File:{l_file_path_new}|AppRefDocNumber:{l_app_ref_doc_num}"
#                 .format(
#                     key=key,
#                     l_file_path_new=l_file_path_new,
#                     l_app_ref_doc_num=l_app_ref_doc_num))
#
#             with open(join(errorDIR, fileMissingLabel), "a+") as f:
#                 f.write(error_message + '\n')
#
#             continue
#         labels_list.append(label_dict[key][1])
#
#     if len(labels_list) == 0:
#         labels_string = 'NA'
#     else:
#         labels_string = "|".join(str(e) for e in labels_list)
#
#     return labels_string


######################## Get the label sub class

def get_label_sub_class(l_file_path_new, l_app_ref_doc_num):
    label_sub_class_list = []
    for key in label_sub_class_lookup_key_list_filtered:
        if key not in label_dict.keys():
            # Checks for missing label keys missing in label source and writes them to error files
            error_message = ("LabelSubClassKey:{key}|File:{l_file_path_new}|AppRefDocNumber:{l_app_ref_doc_num}"
                .format(
                    key=key,
                    l_file_path_new=l_file_path_new,
                    l_app_ref_doc_num=l_app_ref_doc_num))
            
            with open(join(errorDIR, fileMissingLabel), "a+") as f:
                f.write(error_message + '\n')
            
            continue
        label_sub_class_list.append(label_dict[key][1])
    
    if len(label_sub_class_list) == 0:
        label_sub_class_string = 'NA'
    else:
        label_sub_class_string = "|".join(str(e) for e in label_sub_class_list)
    
    return label_sub_class_string


######################## Remove existing files
def remove_files(dir_list=[], remove_zip=False):
    new_dir_list = []
    if remove_zip is True:
        new_dir_list = [dir_name + "_zipped" for dir_name in dir_list]
    new_dir_list.extend(dir_list)
    for dir_name in new_dir_list:
        print("remove_files: working on {}".format(dir_name))
        if os.path.exists(dir_name) is False:
            continue
        
        for filename in os.listdir(dir_name):
            filepath = os.path.join(dir_name, filename)
            try:
                shutil.rmtree(filepath)
            except OSError:
                os.remove(filepath)


######################## Zip output files
def zip_output(dir_list=[]):
    for dir_name in dir_list:
        zipDIR = dir_name + "_zipped"
        
        if os.path.exists(zipDIR) is False:
            os.makedirs(zipDIR)
        for root, directories, files in os.walk(dir_name):
            for filename in files:
                filepath = os.path.join(root, filename)
                with open(filepath, 'rb') as f_in:
                    with gzip.open(os.path.join(zipDIR, filename + ".gz"), 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)


######################## MAIN ########################

config = configparser.ConfigParser()
config.read('../config/preparation.ini')

inDIR = config['DEFAULT']['inDIR']
pattern = config['DEFAULT']['pattern']
outDIR = config['DEFAULT']['outDIR']
errorDIR = config['DEFAULT']['errorDIR']
labelDIR = config['DEFAULT']['labelDIR']
logDIR = config['DEFAULT']['logDIR']

fileNameToDocNumber = config['DEFAULT']['fileNameToDocNumber']
fileDocNumberToClassText = config['DEFAULT']['fileDocNumberToClassText']
fileDocNumberToInvTitle = config['DEFAULT']['fileDocNumberToInvTitle']
fileDocNumberToAbsText = config['DEFAULT']['fileDocNumberToAbsText']
fileDocNumberToDescText = config['DEFAULT']['fileDocNumberToDescText']
fileDocNumberToClaimText = config['DEFAULT']['fileDocNumberToClaimText']
fileDocNumberToLabels = config['DEFAULT']['fileDocNumberToLabels']
fileDocNumberToLabelSubClass = config['DEFAULT']['fileDocNumberToLabelSubClass']
fileDocNumberToLabelSubClassCode = config['DEFAULT']['fileDocNumberToLabelSubClassCode']

fileMissingLabel = config['DEFAULT']['fileMissingLabel']

labelPattern = config['DEFAULT']['labelPattern']
limit_files_write = config.getint('DEFAULT', 'limit_files_write')
path_string_to_replace = config['DEFAULT']['path_string_to_replace']
limit_word_count = config.getint('DEFAULT', 'limit_word_count')

label_sub_class_filter = config['DEFAULT']['label_sub_class_filter']

fileList = []
doc_number_filename = defaultdict(list)
cnt_files = 0

log_file = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".log"

#### Read label files
# label_pattern_to_replace defines everything within brackets. Such text, including the brackets will be deleted.
label_pattern_to_replace = re.compile("\(.*\)")
label_dict = {}
label_dict = read_label_files()

# For brevity in output file fileNameToDocNumber.txt
pattern_path = re.compile("^" + path_string_to_replace)

# Accepting labels with filter
regex_label_filter = re.compile('^'+label_sub_class_filter)

# Remove existing files. The logic will also consider *_zipped directories

dir_to_delete_list = [outDIR, errorDIR]
remove_files(dir_to_delete_list, remove_zip=True)

docNumber_date_dict = {}
for dName, sdName, fList in os.walk(inDIR):
    outer_break_flag = 0
    for fileName in fList:
        # Match search pattern
        if fnmatch.fnmatch(fileName, pattern):
            
            # Controls the number of files read
            if cnt_files == limit_files_write:
                outer_break_flag = 1
                break
            
            file_path = join(dName, fileName)
            file_path_new = re.sub(pattern_path, '', file_path)

            try:
                tree = ET.parse(file_path)
            except:
                error_message = "Tree error for file:"+file_path
                with open(join(errorDIR, fileMissingLabel), "a+") as f:
                     f.write(error_message + '\n')
                continue
                
            root = tree.getroot()
            app_ref_doc_num = get_app_ref_doc_number()
            application_date = get_application_date()
            
            # Ignoring if patent with same application number has been seen
            if app_ref_doc_num in docNumber_date_dict.keys():
                existing_patent_date = docNumber_date_dict[app_ref_doc_num]
                with open(join(logDIR, log_file), "a+") as f:
                    write_str = ("doc-number {}, application_date {} has been seen with date {}".format(app_ref_doc_num,
                                                                                                        existing_patent_date,
                                                                                                        application_date))
                    f.write(write_str + '\n')
                continue
            
            docNumber_date_dict[app_ref_doc_num] = application_date
            
            # label_lookup_key_list = []
            label_sub_class_lookup_key_list = []
            label_sub_class_lookup_key_string=''
            label_sub_class_lookup_key_list = get_classification_ipcr()

            label_sub_class_lookup_key_list_filtered = [element for element in label_sub_class_lookup_key_list if regex_label_filter.search(element)]

            # if len(label_sub_class_lookup_key_list) == 0 or not (all(ele.startswith(label_sub_class_filter) for ele in label_sub_class_lookup_key_list)):
            #     continue

            if len(label_sub_class_lookup_key_list_filtered) == 0:
                # label_sub_class_lookup_key_string = '|'.join(str(e) for e in label_sub_class_lookup_key_list)
                # error_message = "Skipped label:"+label_sub_class_lookup_key_string+" for file:"+file_path_new
                # with open(join(errorDIR, fileMissingLabel), "a+") as f:
                #     f.write(error_message + '\n')
                continue

            label_sub_class_lookup_key_string = '|'.join(str(e) for e in label_sub_class_lookup_key_list_filtered)


            # labels = get_labels(file_path_new, app_ref_doc_num)
            label_sub_class = get_label_sub_class(file_path_new, app_ref_doc_num)
            
            if label_sub_class == 'NA':
                continue
            
            inv_title = get_invention_title()
            if inv_title == 'NA':
                continue
            
            abstract_text = get_abstract_text()
            if abstract_text == 'NA':
                continue
            
            desc_text = get_description_text()
            if desc_text == 'NA':
                continue
            
            claim_text = get_claim_text()
            if claim_text == 'NA':
                continue
            
            cnt_files = cnt_files + 1
            
            write_files()
    
    if outer_break_flag == 1:
        break

# Compress output for sharing.
dir_to_zip_list = [outDIR, errorDIR, logDIR]
zip_output(dir_to_zip_list)

# Not removing zipped files
remove_files(dir_to_zip_list)
