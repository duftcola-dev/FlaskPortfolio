

from .dependencies.Logs import Logs
from inspect import getframeinfo,currentframe
import pymongo

class MgDriver(Logs):

    def __init__(self,log_class,database:str,table:str,id,data) :
        self.logs=log_class
        self.client=pymongo.MongoClient("mongodb+srv://robin:robin123@flaskportfolio.5qs12.mongodb.net/test?retryWrites=true&w=majority")
        self.client.test
        self.__database=self.client[str(database)]
        self.__table=self.__database[table]
        self.database_name=database
        self.table_name=table 
        self.current_file=self.__GetCurrentFile()   
        if self.__DatabaseExist()==True:
            self.LogMessage("warning","Database already exist",self.current_file)
        else:
            self.__InsertIntoCollection(id,data)
            self.LogMessage("info","Database created : "+self.database_name,self.current_file)





    def AddOneIntoCollection(self,id,data:dict):

        if not self.__DataTypeStr(data):
            self.LogMessage("info","Inserting into"+self.table_name+" "+str(data),self.current_file)   
        else:
            self.LogMessage("info","Inserting into"+self.table_name+" "+data,self.current_file)


        if not self.__DatabaseExist():
            self.LogMessage("warning","Database doesnt exist , insert aborted",self.current_file)
            return False
        
        if not self.__CollectionExist():
            self.LogMessage("warning","Collection doesnt exist , insert aborted",self.current_file)
            return False

        inserted_items=self.__InsertIntoCollection(id,data)
        self.LogMessage("info","Items added to table : "+self.table_name+" | items : "+str(inserted_items),self.current_file)
        return inserted_items
       



    def AddManyIntoColleciton(self,data:list):

        if type(data) is not list:
            self.LogMessage("warning","Insert many into collection requires list data type",self.current_file)
            return False

        if not self.__DatabaseExist():
            self.LogMessage("warning","Database doesnt exist , insert aborted",self.current_file)
            return False
        
        if not self.__CollectionExist():
            self.LogMessage("warning","Collection doesnt exist , insert aborted",self.current_file)
            return False

        inserted_items=self.__InsertManyIntoCollection(data)
        self.LogMessage("info","Items inserted into "+self.table_name+" | items:"+str(inserted_items),self.current_file)
        return inserted_items





    def NewTable(self,table,id,data):
        
        if not self.__DataTypeStr(table):
            self.LogMessage("warning","table must be a string with a name",self.current_file)
            return False

        self.database_name=table
        self.__table=self.__database[table]

        if not self.__DatabaseExist():
            self.LogMessage("warning","Database doesnt exist , Creater database before creating table",self.current_file)
            return False
            
        if self.__CollectionExist():
            self.LogMessage("warning","Collection already exist",self.current_file)
            return False
        
        self.__InsertIntoCollection(id,data)
        self.LogMessage("info","New table created : "+self.table_name+" in database "+self.database_name,self.current_file)
   
  



    def GetData(self,table,key,value):
        
        if not self.__DataTypeStr(table):
            self.LogMessage("warning","table must be a string with the name of a collection",self.current_file)
            return False


        self.table_name=table
        self.__table=self.__database[table]

        if not self.__DatabaseExist():
            self.LogMessage("warning","Data cannot be retrieved, database doesnt exist :"+self.database_name,self.current_file)
            return False
        if not self.__CollectionExist():
            self.LogMessage("warning","Data cannot be retrieved, collection doesnt exist :"+self.table_name,self.current_file)
            return False

        items=self.Find(table,key,value)
        result=""
        for item in items:
            result=item
        
        if result =="":
            self.LogMessage("info","Data not found",self.current_file)
            return False

        self.LogMessage("info","Data retrieved",self.current_file)
        return result["data"]
            
   

    def SaveChanges(self,table,key,value,data):
        
        if not self.__DataTypeStr(table):
            self.LogMessage("warning","table must be a string with the name of a collection",self.current_file)
            return False

        self.table_name=table
        self.table=self.__database[table]
        
        if not self.__DatabaseExist():
            self.LogMessage("warning","Data cannot be saved, database doesnt exist :"+self.database_name,self.current_file)
            return False

        if not self.__CollectionExist():
            self.LogMessage("warning","Data cannot be saved, collection doesnt exist :"+self.table_name,self.current_file)
            return False

        self.__Update(table,key,value,data)
        self.LogMessage("info","Data updated -> database:"+self.database_name+" --> table "+self.table_name,self.current_file)



    def __DatabaseExist(self)->bool:

        databases=self.client.list_database_names()
        if self.database_name in databases:
            return True

        return False



    def __CollectionExist(self):

        collections=self.__database.list_collection_names()

        if self.table_name in collections:
            return True

        return False



    def __InsertIntoCollection(self,id,data):

        temp={
            "_id":id,
            "data":data
        } 
        item_id=self.__table.insert_one(temp)
        return item_id



    def __InsertManyIntoCollection(self,items:list):

        items_id=self.__table.insert_many(items)
        return items_id



    def Find(self,table:str,key:str,value:str):
        
        if not self.__DataTypeStr(table):
            self.LogMessage("warning","table must be a string with the name of a collection",self.current_file)
            return False

        self.table_name=table
        self.__table=self.__database[table]
        
        query={ str(key):str(value)}
        items=self.__table.find(query)
        return items



    def FindOne(self,table):

        if not self.__DataTypeStr(table):
            self.LogMessage("warning","table must be a string with the name of a collection",self.current_file)
            return False

        self.__table=self.__database[table]
        item=self.__table.find_one()
        return item



    def FindAll(self,table):

        if not self.__DataTypeStr(table):
            self.LogMessage("warning","table must be a string with the name of a collection",self.current_file)
            return False

        self.__table=self.__database[table]
        items=self.__table.find()
        return items



    def DeleteOne(self,table,key,value):

        if not self.__DataTypeStr(table):
            self.LogMessage("warning","table must be a string with the name of a collection",self.current_file)
            return False

        self.__table=self.__database[table]
        query={str(key):str(value)}
        deleted_item=self.__table.delete_one(query)
        return deleted_item 



    def DeleteAll(self,table):

        if not self.__DataTypeStr(table):
            self.LogMessage("warning","table must be a string with the name of a collection",self.current_file)
            return False

        self.__table=self.__database[table]
        deleted_items=self.__table.delete_many({})
        return deleted_items


    def DeleteCollection(self,table):

        if not self.__DataTypeStr(table):
            self.LogMessage("warning","table must be a string with the name of a collection",self.current_file)
            return False

        self.__table=self.__database[table]
        deleted_table=self.__table.drop()

        result=self.__CollectionExist()

        return deleted_table,result

    

    def __DataTypeStr(self,data):

        if type(data) is not str:
            return False
        
        return True



    def __Update(self,table,key,value,data):
        
        items=self.Find(table,key,value)
        result=""
        for x in items:
            result=x
        result=result.get("data")
        query={"data":result}
        new_value={ "$set": {"data":data}}
        self.__table.update(query,new_value)



    def __GetCurrentFile(self):

        cf=currentframe()
        currentfile=getframeinfo(cf).filename
        start=currentfile.rfind("\\")+1
        end=len(currentfile)
        string=""
        for char in range(start,end):

            string=string+currentfile[char]

        return string



