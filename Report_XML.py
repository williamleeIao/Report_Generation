import xml.etree.ElementTree as ET
import subprocess
import ntpath
import os
import shutil
import tkinter as tk
from tkinter import filedialog
import xlwings as xw
import re

Library_section={}
Library_temperature_section={}

# XML Function -done
def load_XML_file(path_source):
    myXMLTree = ET.parse(path_source)
    return myXMLTree

#This is read op seq file
def Read_XML_Op_Seq(XML_Tree):
    dict_op = {}
    myroot = XML_Tree.getroot()
    for op_seq in myroot.iter('Test_Suite_Data'):
        dict_op["OP_SEQ"] = op_seq.attrib['Name']
    return dict_op

def Read_XML_Results(XML_Tree):
    ls_all_test=[]

    dict_single_test = {}
    myroot = XML_Tree.getroot()
    for x in myroot.iter('Test_Case_Result'):
        for test_name in x.iter('Test_Case_Data'):
            dict_single_test['Test_Name'] = test_name.attrib['Name']
            print(test_name.attrib)
            for y in x.iter("Parameters"):
                for z in y.iter("Parameter"):
                    for p1 in z.iter("Actual_Parameter"):
                        #dict_single_test[p1.attrib['Name']] = p1.attrib['Name']
                        print(p1.attrib, " ")
                        # if loop then one more time insert it
                        loop_ctr = 0  # initliaze loop_ctr
                        for value in p1.iter("Value"):
                            if loop_ctr == 0:
                                dict_single_test[p1.attrib['Name']] = value.text
                            else:
                                 if not( value.text is None):
                                     dict_single_test[p1.attrib['Name']] = dict_single_test[p1.attrib['Name']] + "," + value.text

                            print(value.text)
                            loop_ctr += 1

            # add into the list and clear current dictionary
            ls_all_test.append(dict_single_test)
            dict_single_test={}  # initiliaze back
    return ls_all_test

# Tdr to XML decompress - done
def tdr_and_xml_file_process(path_source):
    single_element=[]
    path_tdr = path_source # This is a tdr file only
    directory , path_xml = ntpath.split(path_source)
    # expect there is a _decompress.tdr for every file
    new_path_xml = path_xml.replace("_COMPRESSED.tdr", ".xml")
    single_element = path_xml.split("_")
    return path_tdr, directory + "\\" + new_path_xml,single_element[2] #2 is the SN

def decompress_process(path_tdr, path_xml,compress_path):
    # String construction ( this is temporary)
    process_to_run = "{} -d \"{}\" \"{}\" ".format(compressFile, path_tdr, path_xml)
    # process_to_run = "C:\\Users\\willlee\\Documents\\Working Tools\\BNTDRGeneratorFiles\\StreamCompressor -d "\
    #                  + " \"" + path_tdr + "\"" + " " + "\"" + path_xml + "\""
    try :
        output2 = subprocess.run(process_to_run)
    except output2.returncode !=0:
        print ("Decompress file not working properly")

# Port Data to notepad file using SN as fileName
def CreateNewFolderAndFile(path_source,SN):
    found = False
    path_tdr = path_source  # This is a tdr file only
    directory, path_xml = ntpath.split(path_source)
    new_directory = directory + "\\" + "results"
    # list_directories = os.listdir(directory)
    # for current_directory in list_directories:
    #     if current_directory == "results":
    #         found = True
    # if not found:
    #     os.mkdir(new_directory)
    return directory

def WritelistIntoFile(directory, SN, list_result,dict_opseq ):
    file_construction = directory + "\\"+ SN + "_result.txt"
    with open(file_construction,"a+") as f:
        op_seq_text = "OP_SEQ : " + dict_opseq["OP_SEQ"]
        f.write(op_seq_text)
        f.write ("\n------------------------------\n")
        # Get from list_result
        for dict_test in list_result:
            #extract the keys value
            test_name_text = "TEST_NAME : " + dict_test["Test_Name"]
            f.write(test_name_text)
            f.write("\n------------------------------\n")
            for i in range(1, len(list(dict_test.keys()))):
                # first key need ignored

                key_value = list(dict_test.keys())[i]
                if not dict_test[key_value] is None:
                    test_value = list(dict_test.keys())[i] + ":" + dict_test[key_value]
                    f.write(test_value + "\n")
            f.write("\n------------------------------\n")


def loading_Library_section():

    Library_section["Wait for 15 Minutes"] = "0"
    Library_section["Record Leakage J1"] = "8"
    Library_section["Record V Tune"] = "10"
    Library_section["Tuning Sensitivity"] = "11"
    Library_section["Record Leakage J2"] = "12"
    Library_section["IF Out Min Frequency"] = "15"
    Library_section["IF Out Max Frequency"] = "16"
    Library_section["Record IF Out 20 dBm"] = "17"
    Library_section["Record IF Out 24"] = "18"
    Library_section["IF Output Variation"] = "19"
    Library_section["Worst Case Spur 45 to 75 MHz"] = "22"
    Library_section["Worst Case Spur 100 to 125 MHz"] = "24"
    Library_section["Record Leakage J3"] = "25"
    Library_section["Minimum RF Input.vi"] = "28"
    Library_section["Find File"] = "0"
    Library_section["Record Leakage J4"] = "30"
    Library_section["Linearity"] = ["33","34","3","6","5"]
    Library_section["Move File"] = "0"
    Library_section["LO Spur"] = "37"
    Library_section["Other Spurs"] = "38"
    Library_section["Record Current"] = "42"
    Library_section["Frequency Drift"] = "43"

def loading_library_temp():
    Library_temperature_section["876"] = "G3" #Data 60 deg C
    Library_temperature_section["871"] = "E3" #Data 25 deg C
    Library_temperature_section["875"] = "F3" #Data 0 deg C
    Library_temperature_section["896"] = "H3" #Post Seal 25c

def txt_populate_To_Excel(main_path_folder,templateFile):
    #load library and load template file if library and template path is empty
    First_Character=""
    SubSeq_Characters=""

    if len(Library_section) ==0 :
        loading_Library_section()

    if len(Library_temperature_section) ==0:
        loading_library_temp()
    #if location_excel_template
    file_location=[]
    file_location = look_for_result_rxtfile(main_path_folder)  # all _result.txt should be in filelocation list
    for single_file in file_location:
        # create a path for excel
        # create template_file_path
        #excel_file_path = os.path.join(main_path_folder,
        if os.path.splitext(single_file)[1] == ".txt":
            template_file = xw.Book(templateFile)
            single_file = single_file.replace("\\","/")
            SN_file_Name = single_file.split("/")[5] + "_report.xlsx"
            # enter the SN into the excel
            template_file.sheets["Sheet1"].range("F2").value = SN_file_Name
            excel_file_name = os.path.join(main_path_folder,  single_file.split("/")[5],SN_file_Name)
            #open txt file
            with open(single_file, "r") as f:
                txtline = f.readline()
                while(txtline):
                    if "OP_SEQ" in txtline:
                        trim_space = re.sub('\s+',' ',txtline.split(":")[1])
                        Home_Excel_Position = Library_temperature_section[trim_space.split()[0]]
                        First_Character= Home_Excel_Position[0:1] # Column Character
                        SubSeq_Characters = Home_Excel_Position[1:]  # digit
                    if "TEST_NAME" in txtline:
                        # location for excel
                        test_name = txtline.split(":")[1]
                        trim_a = re.sub("\s+", ' ', test_name).strip()
                        location = Library_section[trim_a]
                        # convert location and SubSeq_Character into Integer
                        if isinstance(location,list):
                            pass
                        else:
                            int_location = int(location)
                            int_home_position = int(SubSeq_Characters)
                            actual_location = First_Character + str(int_location + int_home_position)
                        while(txtline != "\n"):
                            txtline = f.readline()
                            if "Scalar Data" in txtline:
                                measurement_value = txtline.split(":")[1].strip()    # split :
                                measurement_value = measurement_value.split(",")[0] # split ,
                                # Check the value and convert the value accordingly to MHz
                                if int_location == 11 or int_location == 43:
                                    # do the conversion to MHz
                                    measurement_value = int(measurement_value) * 1e-6
                                template_file.sheets["Sheet1"].range(actual_location).value = measurement_value
                            if "Data cluster" in txtline:
                                measurement_value = txtline.split(":")[1].strip()  # split :
                                measurement_value_list = measurement_value.split(",")
                                for idx, measurement_value in enumerate(measurement_value_list):
                                #for i in range(0, len(measurement_value_list)):  #replace with upper for
                                    actual_location =  First_Character + str(int(location[idx]) + int_home_position)
                                    template_file.sheets["Sheet1"].range(actual_location).value = measurement_value_list[idx]
                    txtline = f.readline()
                template_file.save(excel_file_name)
            template_file.close()

def look_for_result_rxtfile(main_path_folder):
    all_result_files=[]
    for root, dirs,files in os.walk(main_path_folder):
        for dir in dirs:
            secondary_path = os.path.join(main_path_folder,dir)
            for sec_root, sec_dir, sec_files in os.walk(secondary_path):
                for sec_file in sec_files:
                    if sec_file.find("_result.txt") !=1 :
                        # found
                        all_result_files.append(os.path.join(secondary_path, sec_file))
    return all_result_files

def File_Cp_To_folder(folder):
    #loop thru the folder
    list_directories = os.listdir(folder)
    # look for _COMPRESSED.tdr only
    for directory in list_directories:
        if directory.find("_COMPRESSED.tdr") != -1:
            # split it to get SN
            SN = directory.split("_")[2]
            # Use this SN look to see whether folder had created
            d = os.path.join(folder, SN)
            # If no directory, make a new one
            if not os.path.isdir(d):
                os.mkdir(d)
           # doing copy file to folder
            source = os.path.join(folder, directory)
            shutil.copy(source, d)


def initialize():
    for root,dirs,files in os.walk(os.getcwd()):
        print (root)
        print (files)
        # look for the below files
        if 'Microsemi data sheet template.xlsx' in files and 'StreamCompressor.exe' in files:
            return True, root + "\\Microsemi data sheet template.xlsx" , root + "\\StreamCompressor.exe"
        return False, None, None

if __name__ == "__main__":
     #File_Cp_To_folder( "C:\\Users\\willlee\\Desktop\\Testing")
     #Initiliaze
     continueToRun, templateFile, compressFile = initialize()
     loading_Library_section()
     loading_library_temp()
     #Done
     loop_ctr = 1
     fileProvided = True
     while (fileProvided):
         root = tk.Tk()
         root.withdraw()
         folder_path = filedialog.askdirectory()
         if os.path.isdir(folder_path): # Main directory
            for root, dirs,files in os.walk(folder_path):
                amount_of_folder = len(dirs)
                for dir in dirs:
                    fileprocess= os.path.join(root, dir)
                    # read the folder
                    # loop thru the folder
                    for single_file in os.listdir(fileprocess):
                        print (single_file)
                        path_tdrA = os.path.join(fileprocess,single_file)
                        path_tdr, path_xml, SN = tdr_and_xml_file_process(path_tdrA)
                        decompress_process(path_tdr, path_xml,compressFile)
                        XMLTree = load_XML_file(path_xml)
                        dict_op = Read_XML_Op_Seq(XMLTree)
                        ls_all_test = Read_XML_Results(XMLTree)
                        new_directory = CreateNewFolderAndFile(path_tdr, SN)
                        WritelistIntoFile(new_directory, SN, ls_all_test, dict_op)
                #main_path_folder = "C:\\Users\\willlee\\Desktop\\Microsemi MVR data"
            txt_populate_To_Excel(folder_path, templateFile)
         else:
             fileProvided = False
         # if os.path.exists(file_path):
         #     orig_file_path = file_path
         #     orig_file_dir = os.path.dirname(file_path)
# Testing on the excel file

    # create window selection
#     path_tdr = "C:\\Users\\willlee\\Desktop\\New folder\\MICR9905101PEN_134435C-01L_3261782_8-22-2022_20-16-23_4438_COMPRESSED.tdr"
#     path_xml = "C:\\Users\\willlee\\Desktop\\New folder\\def.xml"
#     path_tdr, path_xml,SN = tdr_and_xml_file_process(path_tdr)
#     decompress_process(path_tdr, path_xml)
#     XMLTree= load_XML_file(path_xml)
#     Read_XML_Op_Seq(XMLTree)
#     Read_XML_Results(XMLTree)
#     print()
#     new_directory= CreateNewFolderAndFile(path_tdr,'3261782')
#     WritelistIntoFile(new_directory,'3261782',ls_all_test,dict_op)