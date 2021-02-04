import os
import re
import enum


directory = "./"
class EnumExtractor:
    def __init__(self, directory):
        """
        This class Finds Enums in files in  a Directory

        Args:
        directroy  : the directory path

        """
        self.directory = directory
        self.list_of_files = []
        self.enums = []

    def __go_through_directory(self):
        """
        This method goes throught the directory and returns all the files with
        the (".c" , ".cpp" , ".h" ,".hpp" ) extensions
        """
        for root, subdirectories, files in os.walk(self.directory):
            for file in files:
                if file.endswith((".c" , ".cpp" , ".h" ,".hpp" )):
                    self.list_of_files.append(os.path.join(root, file))

    def Find_Enums(self):
        """
        This method finds the enums from the files
        and returns a list of enums
        """
        pattern = r"enum [^;]+" #defining Enums pattern
        EnumExtractor.__go_through_directory(self)
        for file in self.list_of_files :
            #opening the file with the path and joining it's lines
            with open(file , 'r') as file:
                filetext = "".join(file.readlines())
            #removing comments, spaces and lines
            filetext = re.sub('\n', ' ', filetext)
            filetext = re.sub(' +', ' ', filetext)
            comm_pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
                                      re.DOTALL | re.MULTILINE)
            filetext = re.sub(comm_pattern ,
                          lambda match: " " if match.group(0).startswith('/') else match.group(0),
                          filetext)

            self.enums= self.enums + re.findall(pattern, filetext )


        return  self.enums


class EnumConverter:
    def __init__(self , enums , filepath):
        """
        This class covnerts the input enums to python Enums
        """
        self.enums = enums
        self.filepath = filepath
    def convert(self):
        """
        This method converts the enums to python and puts them in  the outupt file
        writes in this form:
        class name(enum.Enum):
            name1 = value1
            name2 = value2
            .
            .
            .
            .

        """
        enums_list = []
        for enum in self.enums :
            #looping and not taking any Enum with # in it
            if not '#' in enum and ('{' in enum ) and ('}' in enum):
                enums_list.append(EnumConverter.__spliting_enum(enum))

        with open(self.filepath , 'w') as f: #opens the file with writing mode
            f.write('import enum\n\n') #imoporting enum in the file for the auto values
            for i in enums_list:
                if i[0] == "{" or i[0] == '': #Some special cases without names
                    name = "NoneName"
                else:
                    name = i[0]
                dictionary = i[1]
                if  bool(dictionary): #dealing with empy dictionary case I found

                    S = f'class {name}(enum.Enum):\n'
                    for n in dictionary:
                        S += f'\t{n} = {dictionary[n]}\n'
                    S += '\n'

                f.write(S)

    @staticmethod
    def __spliting_enum(enum):
        """
        Takes enum as an argument
        This method retruns a tuple with name and a dictionary with the items in it
        """
        enum_l = enum.split('}')
        if  enum_l[1] != "}" :
            name = enum_l[1]
        else:
            enum_f = enum_l[0].split(' ')
            name = enum_f[1]
        enum_e = enum.split('{' , 1 )
        enum_elements = (enum_e[1].split("}"))[0]
        enum_elements = enum_elements.split(',')
        elements  = EnumConverter.__element_dict(enum_elements)
        return name , elements
    @staticmethod
    def __element_dict(elements):
        """
        This Method takes enum elements as an argument and returns them as a dictionary
        """
        elements_dict = dict()
        for element in elements:
            element = element.strip()
            if "=" in element :
                item , value =  element.split('=')
                item = item.strip()
                value = value.strip()
                if value[0].isdigit():
                    elements_dict[item] = value
            elif len(elements) > 0 :
                item  = element.strip()
                value = 'enum.auto()'
                elements_dict[item] = value
        return elements_dict






#x = EnumExtractor("./")


#z = x.Find_Enums()
#y = EnumConverter(z , 'output.py')
