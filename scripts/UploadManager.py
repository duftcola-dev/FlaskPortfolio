import os
from inspect import getframeinfo,currentframe
import sys

from werkzeug.datastructures import RequestCacheControl

class Upload:

    def __init__(self,log_class) -> None:
        self.current_file=self.__GetCurrentFile()
        self.logs=log_class
        self.search_file_result=""
        self.last_deleted_file=""
        self.AllowedExtensions=['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']


    def IsFileAllowed(self,files:list):

        self.logs.LogMessage("info","Upload : checking files data types",self.current_file)

        for file in files:
            
            start=file.filename.find(".")+1
            end=len(file.filename)
            extension=""

            for char in range(start,end):

                extension=extension+file.filename[char]

            extension=extension.lower()

            if extension not in self.AllowedExtensions:
                self.logs.LogMessage("warning","Upload : File data type not allowed, canceling upload",self.current_file)
                return False
        
        return True



    def SearchFile(self,file_name,files_list):
        self.logs.LogMessage("info","Searching file "+file_name,self.current_file)
        for file in files_list:
            print(file)
        if file_name in files_list:
            self.search_file_result=file_name
            return file_name
        self.logs.LogMessage("info","File not found",self.current_file)
        return False




    def GetUploadPath(self,form,registry):
        self.logs.LogMessage("info","Upload : Selecting upload folder path",self.current_file)
        selected_folder=""
        for folder in form:
            selected_folder=folder
        
        if selected_folder in registry:

            result=registry.get(selected_folder)
            self.logs.LogMessage("info","Upload : Files will be uploaded to "+selected_folder,self.current_file)
            return result
         
        
        self.logs.LogMessage("error","Upload : The selected folder : "+selected_folder+" no longer exists in this app",self.current_file)
        return False




    def DeleteFile(self,files):

        if self.search_file_result=="":
            self.last_deleted_file=""
            return False
            
        else:
            try:
                path=files.get(self.search_file_result)
                os.remove(path)
                self.last_deleted_file=self.search_file_result
                self.search_file_result==""
                return True
            except:
                self.logs.LogMessage("error","Cannot remove file,wrong path or file doesnt exist",self.current_file)
                self.last_deleted_file=""
                return -1


    def __GetCurrentFile(self):

        system_symbol=""
        if sys.platform == "linux":
            system_symbol="/"
        else:
            system_symbol="\\"
        
        cf=currentframe()
        currentfile=getframeinfo(cf).filename
        start=currentfile.rfind(system_symbol)+1
        end=len(currentfile)
        string=""
        for char in range(start,end):

            string=string+currentfile[char]

        return string
