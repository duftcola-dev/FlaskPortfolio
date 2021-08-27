import abc
import os
import sys
# Author Robin Viera 
# Data 07/05/2021
# Description: This class scan directories recursively and creates a directory tree as a result
# in the form of a list of strings



class Interface_MetaDir(abc.ABC):

    @classmethod
    def __subclasshook__(cls,subclass):
        
        return (hasattr(subclass,"ExploreDirectories"))

    @abc.abstractmethod
    def ExploreDirectories(self,path:str)->bool:
        "set path root for path explorer, returns tow lists elements"
        raise NotImplemented



class TreeExplorer(Interface_MetaDir):



    def __init__(self):

        self.Files_Registry={}
        self.Dir_Registry={}
        self.Files_List=[]
        self.Dir_List=[]
        self.Dir_Map=[]
        self.w_slash=""
        self.path=""
        self.new_path=""



    def ExploreDirectories(self,path:str="",mode:str="absolute",ignore="")->list:
        
        self.ignore_dir=ignore
        self.Files_Registry={}
        self.Dir_Registry={}
        self.Files_List=[]
        self.Dir_List=[]
        self.Dir_Map=[]
        
        if sys.platform == "linux":
            self.w_slash="/"
        else:
            self.w_slash="\\"

        current_dir=""
        if path=="" and mode=="":  
            current_dir=os.getcwd()
        elif mode=="absolute" and  path !="":
            current_dir=path
        elif mode=="relative" and path !="":
            current_dir=os.getcwd()
            current_dir=current_dir+self.w_slash+path

        if os.path.isdir(current_dir):
            self.path=current_dir
            self.__Explore_Directories(self.path)
        else:
            return False
            




    def __Explore_Directories(self,root:str):

        Current_Dir_Entries=os.scandir(root)

        for entry in Current_Dir_Entries:

            if self.ignore_dir !="":
                if entry.name==self.ignore_dir:
                    continue

            self.new_path=root+self.w_slash+entry.name
  
            name=str(entry.name)
            path=str(entry.path)
            
            if entry.is_dir():
                
                self.Dir_Registry.update({name:path})
                self.Dir_List.append(path)
                self.__Explore_Directories(self.new_path)
            else:
                self.Files_Registry.update({name:path})
                self.Files_List.append(path)

       
