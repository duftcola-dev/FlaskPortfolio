
import json
import os
from cryptography.fernet import Fernet

class UserAccess:


    def __init__(self,path) -> None:
  
        self.path=path
        self.app_key=""
 

    def CheckCredentials(self,user,password):

        u,p=self.__GetCredentials()

        if u==user and p==password:
            return True

        return False


    def GetItem(self,item):

        file=open(self.path,"r")
        content=file.read()
        content=json.loads(content)

        key=content.get("key")
        key=key.encode()
        self.fernet=Fernet(key)

        result=key=content.get(item)
        result=result.encode()
        result=self.fernet.decrypt(result).decode()
        file.close()

        return result


    def __GetCredentials(self):
        file=open(self.path,"r")
        content=file.read()
        content=json.loads(content)

        key=content.get("key")
        key=key.encode()
        self.fernet=Fernet(key)

        user= content.get("user")
        password= content.get("password")

        user=user.encode()
        password=password.encode()

        user=self.fernet.decrypt(user).decode()
        password=self.fernet.decrypt(password).decode()
        file.close()

        
        return user,password


