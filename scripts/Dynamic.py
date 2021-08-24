import os
from werkzeug.datastructures import iter_multi_items
from inspect import getframeinfo,currentframe
from .dependencies.Logs import Logs
from .dependencies.DirectoryTreeGenerator import TreeExplorer



class DynamicContent(TreeExplorer,Logs):

    def __init__(self,Log_class,images_url="\\static\\content\\") -> None:
        super().__init__()
        self.current_file=self. __GetCurrentFile()
        self.logs=Log_class
        self.galleries_thumbnails={}
        root=os.getcwd()
        self.images_url=root+images_url
        self.save_in_folders=[]
        self.urls=[]
        self.internal_urls={}
        self.search_file_result=""
        self.last_deleted_file=""
        self.AllowedExtensions=['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

        self.UploadPath={
            "RED":root+"\\static\\content\\RED\\",
            "ASSETS":root+"\\static\\content\\ASSETS\\",
            "GRAY":root+"\\static\\content\\GRAY\\",
            "ORANGE":root+"\\static\\content\\ORANGE\\",
            "BLUE":root+"\\static\\content\\BLUE\\",
            "OTHERS":root+"\\static\\content\\OTHERS\\",
            "THUMBNAILS":root+"\\static\\content\\THUMBNAILS\\"
        }
        self.blueprint={
            "ROOT":{},
            "THUMBNAILS":{},
            "COlORS":{},
            "BLUE":{},
            "GRAY":{},
            "ORANGE":{},
            "OTHERS":{},
            "RED":{},
            "ASSETS":{}
        }
        self.colors={
            "Default":["primary","danger","warning","success","secondary"],
            "MainTheme":["MainBlue","MainRed","MainOrange","MainGray","MainWhite"],
            "BlueTheme":["Orange500","Orange400","Orange300","Orange200","LightGray"],
            "OrangeTheme":["Red","Crimson", "Pink","RedGray200","RedGray100"],
            "RedTheme":["Blue500","Blue400","Blue300","Blue200","Brown"],
            "GrayTheme":["DarkBlue","Gray500","Gray400","Gray300","Gray200"]
        }

#Clears the blueprint dict .
#Search for al the urls in the folder content
#update the blueprint dictionary


    def UpdateBlueprint(self)->dict:
        
        self.LogMessage("info","Updating themes and data in folders",self.current_file)
        self.ClearBlueprint()
        self.__FormatImgUrl(self.images_url)
        self.__UpdateUrlList()
        return self.blueprint



    def ClearBlueprint(self):
        
        self.blueprint={
            "ROOT":{},
            "THUMBNAILS":{},
            "COlORS":{},
            "BLUE":{},
            "GRAY":{},
            "ORANGE":{},
            "OTHERS":{},
            "RED":{},
            "ASSETS":{}
        }

    
    def GetColors(self,item):

        return self.colors.get(item)


    def GetCollection(self,collection)->dict:

        return self.blueprint[str(collection)]



#Searches for a collection in the blueprint dictionary
# Adds the first 3 elements in that collection to an array/list + an url . Then the list is added as
# a new object inside a new dictionary
    def GetGalleriesThumbnails(self,collection_name:str,theme_url:str)->dict:
       
        self.LogMessage("info","getting galleiers thumbnails",self.current_file)
        new_array=[]
        collection=self.blueprint[str(collection_name)]
        i=-1
        for url in collection:
            i=i+1
            new_array.append(collection[url])

            if i==2:
                break
        new_array.append(theme_url)
        self.galleries_thumbnails.update({collection_name:new_array})



    def IsFileAllowed(self,files:list):

        self.LogMessage("info","Upload : checking files data types",self.current_file)

        for file in files:
            
            start=file.filename.find(".")+1
            end= len(file.filename)
            extension=""
            for char in range(start,end):

                extension=extension+file.filename[char]

            extension=extension.lower()

            if extension not in self.AllowedExtensions:
                self.LogMessage("warning","Upload : File data type not allowed, canceling upload",self.current_file)
                return False
        
        return True



#Returns all the files currently stored in the content folder
    def ShowFiles(self):

        return self.internal_urls.keys()



    def DeleteFile(self):

        if self.search_file_result=="":
            self.last_deleted_file=""
            return False
            
        else:
            try:
                os.remove(self.search_file_result)
                self.last_deleted_file=self.search_file_result
                self.search_file_result==""
                return True
            except:
                self.LogMessage("error","Cannot remove file,wrong path or file doesnt exist",self.current_file)
                self.last_deleted_file=""
                return -1



# Searches for a file among the ones already registered during the content update process. 
# In order to update the list another content update process must be executed
    def SearchFile(self,filename):

        self.search_file_result=""
        if filename in self.internal_urls:

            self.search_file_result=self.internal_urls.get(filename)
            return filename
        else:
            return False



#Checks the folders selected in the form and saves a file or copy 
# of the file in each selected folder
    def GetUploadFolderPath(self,folders:list):
        
        self.save_in_folder=[]
        path=""
        for folder in folders:
            if folder in self.UploadPath:
                path=self.UploadPath.get(folder)

        return path




#Searches all the urls inside the specified directory
#Finds the name content and from that name converts all \\ characters into /
# Adds the transformed string to a list 
    def __FormatImgUrl(self,url):
  
        self.Define_Root_Path_Folder(url,"absolute")
        self.__CreateFilesRegistry(self.Dir_List)
        self.urls=[]
        

        for dir in self.Dir_List:
            
            start=dir.find("content")
            end=len(dir)
            string=""

            for char in range(start,end):
                
                if(dir[char]=="\\"):
                    string=string+"/"
                else:
                    string=string+dir[char]
            string="/"+string
            self.urls.append(string)
        
        


# If an url inside the list urls contains the name of one of the items
#inside the dictonary blueprint then the url is added to this item
    def __UpdateUrlList(self):
        
        count=0
        for url in self.urls:

            for folder in self.blueprint:
                
                if not url.find(folder)==-1:
                    
                    i="item"+str(count)
                    self.blueprint[folder][i]=url
                    count+=1


# dictionary created for the search of files. Contains the name of the files + its url
    def __CreateFilesRegistry(self,urls:list):
        
        self.internal_urls={}
        for full_url in urls:

            start=full_url.rfind("\\")+1
            end=len(full_url)
            file_name=""

            for char in range(start,end):

                file_name=file_name+full_url[char]
              
            self.internal_urls.update({file_name:full_url})


    def __GetCurrentFile(self):

        cf=currentframe()
        currentfile=getframeinfo(cf).filename
        start=currentfile.rfind("\\")+1
        end=len(currentfile)
        string=""
        for char in range(start,end):

            string=string+currentfile[char]

        return string
