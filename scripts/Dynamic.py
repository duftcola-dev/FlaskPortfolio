import sys
from inspect import getframeinfo,currentframe



class DynamicContent():

    def __init__(self,Log_class) -> None:
        self.current_file=self.__GetCurrentFile()
        self.system_symbol=self.__GetSystemSymbol()
        self.__galleries_thumbnails={}
        self.__picturesurls={}
        self.__uploadpath={}
        self.__contentfiles={}
        self.logs=Log_class
        self.colors={
            "Default":["primary","danger","warning","success","secondary"],
            "MainTheme":["MainBlue","MainRed","MainOrange","MainGray","MainWhite"],
            "BlueTheme":["Orange500","Orange400","Orange300","Orange200","LightGray"],
            "OrangeTheme":["Red","Crimson", "Pink","RedGray200","RedGray100"],
            "RedTheme":["Blue500","Blue400","Blue300","Blue200","Brown"],
            "GrayTheme":["DarkBlue","Gray500","Gray400","Gray300","Gray200"]
        }

# GET METHODS

    def GetColors(self,item):

        return self.colors.get(item)


    def GetThemeUrls(self,theme_name:str)->dict:

        return self.__picturesurls[str(theme_name)]


    def GetPicturesUrls(self):

        return self.__picturesurls

    
    def GetUploadPathUrls(self):

        return self.__uploadpath

    def GetContentFilesUrls(self):

        return self.__contentfiles

    def GetGalleriesThumnails(self):

        return self.__galleries_thumbnails


#SET METHODS
    def DefineContentFolders(self,dir_registry:dict):
        self.logs.LogMessage("info","Initializing app content files",self.current_file)
        for keys in dir_registry:

            self.__contentfiles.update({keys:[]})
            self.__uploadpath.update({keys:dir_registry[keys]})
            self.__galleries_thumbnails.update({keys:[]})#contentfiles is a dict of arrays each array with 3 images_urls + a button link
            self.__picturesurls.update({keys:[]})




    def DefineContentUrls(self,files_registry:dict):
        
        self.logs.LogMessage("info","Defining files internal urls",self.current_file)
        for folder in self.__contentfiles:

            for file in files_registry:

                if folder in files_registry[file]:

                    self.__contentfiles[folder].append(files_registry[file])



    def DefineUploadPathUrls(self,dir_registry:list):
        
        self.logs.LogMessage("info","Content folders path for files uploads",self.current_file)
        for folder in dir_registry:

            self.__uploadpath[folder]=dir_registry[folder]+self.system_symbol



    def DefinePicturesUrls(self,files_list:list):
        self.logs.LogMessage("info","Defining in browser pictures urls",self.current_file)
        new_path_list=self.__FormatPicturesUrls(files_list)

        for folder in self.__picturesurls:

            for path in new_path_list:

                if folder in path:

                    self.__picturesurls[folder].append(path)

        self.__DefineGalleriesThumbnails(self.__picturesurls)

    def __FormatPicturesUrls(self,collection:dict):
        self.logs.LogMessage("info","Formating in browser pictures urls",self.current_file)
        search_param="content"
        temp_array=[]
        for string in collection:

            start=string.rfind(search_param)-1
            end=len(string)
            temp_string=""
            for char in range(start,end):

                temp_string=temp_string+string[char]
            temp_array.append(temp_string)
      
        return temp_array

        


    def __DefineGalleriesThumbnails(self,picturesurls:list)->dict:
        self.logs.LogMessage("info","Selecting galleries thumbnails",self.current_file)
        count=0
        for folders in picturesurls:
            count=0
            for files in self.__picturesurls[folders]:
                
                count+=1
                self.__galleries_thumbnails[folders].append(files)
                if count==3:
                    break
        self.__galleries_thumbnails.pop("THUMBNAILS")# we dont need these ones



    def SetGalleryThumbnailsLink(self,gallery_name:str,theme_link:str):

        if gallery_name in self.__galleries_thumbnails:

            self.__galleries_thumbnails[gallery_name].append(theme_link)


    def __GetSystemSymbol(self):

        system_symbol=""
        if sys.platform == "linux":
            system_symbol="/"
        else:
            system_symbol="\\"

        return system_symbol


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
