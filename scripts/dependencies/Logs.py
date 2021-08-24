import sys
import datetime
from inspect import getframeinfo,currentframe

class Logs:

    def __init__(self) -> None:
        pass


    def LogMessage(self,message_type,message,file=""):

        self.type=["warning","error","info"]
        self.message=""
        self.Year=0
        self.Month=0
        self.Day=0
        self.Hour=0
        self.Minute=0
        self.Second=0

        if message_type in self.type:
            frameinfo=currentframe()
            currentline=str(frameinfo.f_back.f_lineno)

            date=self.GetDate()
            self.message=date+" --> "+message_type+"| "+file+" line --> "+currentline+" --> "+message
            print("(INTERNAL) "+self.message)
            self.message="(SYSTEM) "+self.message
            sys.stdout.write(self.message)



    def SaveLogMessage(self):
        message={
            "_id":self.GetDate(),
            "data":self.message
        }

        return message




    def GetDate(self):
        
        x=datetime.datetime.now()
        self.Year=str(x.year)
        self.Month=str(x.month)
        self.Day=str(x.day)
        self.Hour=str(x.hour)
        self.Minute=str(x.minute)
        self.Second=str(x.second)
        
        return self.Year+self.Month+self.Day+self.Hour+self.Minute+self.Second+"-"+self.Day+"|"+self.Month+"|"+self.Year+" - "+self.Hour+":"+self.Minute+":"+self.Second