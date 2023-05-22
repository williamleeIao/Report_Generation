import xml.etree.ElementTree as ET
from collections import UserDict
from dataclasses import dataclass,field
from typing import Dict,List,Optional

class TestDictionary(UserDict):

    def __setitem__(self, key, value):
        print ("Set Item at Here")
        try:
            super().__setitem__(key,value)
        except KeyError:
            print("Cannot write the content to the dictionary")

    def __getitem__(self, key):
        print ("Get Item from here")
        try:
            return super().__getitem__(key)
        except KeyError:
            print("Cannot retrieve the content from dictionary. Please check content")



@dataclass()
class XMLDictContainer:
    key : str = ""
    value : str = None


    def __str__(self):
        '''Display Verbose Output'''
        return f'{self.key} with {self.value}'

    # @property
    # def key(self):
    #     return self.key
    #
    # @property
    # def value(self):
    #     return self.value

@dataclass()
class TestInfo:
    TestInfoDict: Dict[str,str] = field(default_factory=dict)

    def AddInsideDictionary(self, valueContainer: XMLDictContainer):
        self.TestInfoDict[valueContainer.key] = valueContainer.value




@dataclass()
class XMLListDictionary:
    #dict_single_test : dict = field(default_factory=lambda:{"key": None})
    #list_test : List[XMLDictContainer] = field(default_factory=list)
    list_test2: List[TestInfo] = field(default_factory=list)


    # Need to write into setter ???
    def append_element_into_list(self,Anydict: XMLDictContainer):
        self.list_test.append(Anydict)

    @property
    def retrieve_element_from_list(self) -> dict:
        return self.list_test[self.__element]

    @retrieve_element_from_list.setter
    def retrieve_element_from_list(self,element: int):
        self.__element = element




@dataclass()
class XMLClass:

    file_path : str
    def __post_init__(self):
        self.XMLTree = ET.parse(self.file_path)

    @property
    def GetXMLTree(self):
        return self.XMLTree

    @property
    def Read_XML_Content(self) -> str:
        self.node_string = ""
        self.rootName = self.XMLTree.getroot()
        for self.child in self.rootName:
            print(self.child.tag)
        self.children = self.rootName.findall(self.child.tag)
        for child in self.children:
            for node in child.getiterator():
                self.node_string = self.node_string + node.tag + "\n"
        return "Parent Name: {0} \n" \
               "Secondary Name: {1} \n" \
               "Remaining Element {2} ".format(self.rootName.tag, self.child.tag, self.node_string)


    def __str__(self):
        '''display content of the result'''
        self.node_string = ""
        self.rootName = self.XMLTree.getroot()
        for self.child in self.rootName:
            print (self.child.tag)
        self.children = self.rootName.findall(self.child.tag)
        for child in self.children:
            for node in child.getiterator():
                self.node_string = self.node_string + node.tag + "\n"
        return "Parent Name: {0} \n" \
            "Secondary Name: {1} \n" \
            "Remaining Element {2} ".format(self.rootName.tag, self.child.tag, self.node_string)

    def ReadXMLTree(self,XML_Tree):
        self.ls_all_test = XMLListDictionary()


        myroot = XML_Tree.getroot()
        for x in myroot.iter('Test_Case_Result'):
            for test_name in x.iter('Test_Case_Data'):
                self.DictTestInfo = TestInfo()
                # dict_single_test.key = 'Test_Name'
                # dict_single_test.value = test_name.attrib['Name']
                self.DictTestInfo['Test_Name'] = test_name.attrib['Name']
                self.DictTestInfo.AddInsideDictionary(dict_single_test)
                # delete instances
                del dict_single_test
                print(test_name.attrib)
                for y in x.iter("Parameters"):
                    for z in y.iter("Parameter"):
                        for p1 in z.iter("Actual_Parameter"):
                            # dict_single_test[p1.attrib['Name']] = p1.attrib['Name']
                            print(p1.attrib, " ")
                            # if loop then one more time insert it
                            loop_ctr = 0  # initliaze loop_ctr
                            for value in p1.iter("Value"):
                                dict_single_test = XMLDictContainer()
                                if loop_ctr == 0:
                                    dict_single_test.key = p1.attrib['Name']
                                    dict_single_test.value = value.text

                                    #dict_single_test[p1.attrib['Name']] = value.text
                                else:
                                    if not (value.text is None):
                                        dict_single_test.key = p1.attrib['Name'] = \
                                            dict_single_test.key = p1.attrib['Name']
                                        #dict_single_test[p1.attrib['Name']] = dict_single_test[
                                        #                                          p1.attrib['Name']] + "," + value.text
                                self.DictTestInfo.AddInsideDictionary(dict_single_test)
                                del dict_single_test
                                print(value.text)
                                loop_ctr += 1
                self.ls_all_test.append_element_into_list(self.DictTestInfo)
                del self.DictTestInfo
        print()

    @property
    def GetElement(self):
        pass
# Dictionary Information
@dataclass()
class SingleElement:
    name: str
    location: any

    # def append(self,name : str):
    #     pass


def WritingLibrary() -> List[SingleElement]:
    # Test_dict = TestDictionary()
    FirstElement = SingleElement("Wait for 15 Minutes", "0")
    SecondElement = SingleElement("Record Leakage J1", "8")
    ThirdElement = SingleElement("Record V Tune", "10")

    # WholeDic = dictionary(FirstElement)
    # WholeDic.append(SecondElement)
    # print (WholeDic)
    #Test_dict["Wait for 15 Minutes"] = "0"
    #Test_dict["Record Leakage J1"] = "8"
    #Test_dict["Record V Tune"] = "10"
    # Test_dict["Tuning Sensitivity"] = "11"
    # Test_dict["Record Leakage J2"] = "12"
    # Test_dict["IF Out Min Frequency"] = "15"
    # Test_dict["IF Out Max Frequency"] = "16"
    # Test_dict["Record IF Out 20 dBm"] = "17"
    # Test_dict["Record IF Out 24"] = "18"
    # Test_dict["IF Output Variation"] = "19"
    # Test_dict["Worst Case Spur 45 to 75 MHz"] = "22"
    # Test_dict["Worst Case Spur 100 to 125 MHz"] = "24"
    # Test_dict["Record Leakage J3"] = "25"
    # Test_dict["Minimum RF Input.vi"] = "28"
    # Test_dict["Find File"] = "0"
    # Test_dict["Record Leakage J4"] = "30"
    # Test_dict["Linearity"] = ["33","34","3","6","5"]
    # Test_dict["Move File"] = "0"
    # Test_dict["LO Spur"] = "37"
    # Test_dict["Other Spurs"] = "38"
    # Test_dict["Record Current"] = "42"
    # Test_dict["Frequency Drift"] = "43"

    return [FirstElement , SecondElement,ThirdElement ]



@dataclass( frozen = True)
class dictionary:
    DictionaryElement :List[SingleElement] = field(default_factory= list)

    def append(self,Element:SingleElement):
        self.DictionaryElement.append(Element)


if __name__ == "__main__":
    dictionaryElement = dictionary()
    print (dictionaryElement)
    ThirdElement = SingleElement("Tuning Sensitivity", "11")
    print ("")
    dictionaryElement.append(ThirdElement)
    print(dictionaryElement)
    print("")
    trd_xml = XMLClass("C:\\Users\\willlee\\Desktop\\MICR9905101PEN_134435C-01L_3261782_8-22-2022_19-12-22_3945.xml")
    print(trd_xml.Read_XML_Content)

    print(trd_xml.ReadXMLTree(trd_xml.GetXMLTree))

    # Test_dict = WritingLibrary()
    # print (Test_dict)
    # print (Test_dict.keys())
