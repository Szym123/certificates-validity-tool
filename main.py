#!/usr/bin/env python3
# -*- coding: utf8 -*-

import subprocess,re
from datetime import datetime,timedelta

#################################################################
Config={
    "InputFile":"list.txt",
    "OutputFile":"final.html",
    "TimeStamp":[60,2]
}
#################################################################

def openFile(Name):
    Dictionary={}

    try:
        File=open(Name,"r")
        # open a file in read mode

        while True:
            Line=File.readline()
            if not Line:
                break
            Tab=Line.split(":")
            Dictionary[Tab[0]]=Tab[1].replace("\n","")
        # read file line by line

        return Dictionary
        # return table of line
    except:
        return -1

#################################################################

def saveFile(Name,Final,NowDate):

    try:
        File=open(Name,"w")
        # open a file in write mode

        File.write("<h1>List of Worning:</h1>")
        # write first line

        for Item in Final:
            File.write("\n")
            File.write("<p>"+Item+"</p>")
            # write information line by line
            
        File.close()
    except:
        print('['+datetime.strftime(NowDate,"%d/%b/%Y %H:%M:%S")+'] "File '+Name+' cannot be opened"')
        pass

#################################################################

def main():
    Counter=0
    FinalMesage=[]
    NowDate=datetime.now()

    print('['+datetime.strftime(NowDate,"%d/%b/%Y %H:%M:%S")+'] "Program start procesing"')
    Dictionary=openFile(Config["InputFile"])
    try:
        StampDate=timedelta(weeks=Config["TimeStamp"][0],days=Config["TimeStamp"][1])
        Pattern=re.compile("^notAfter=.+")
        # setting of constants
        for Line in Dictionary:
            Adress=Line
            Port=Dictionary[Line]
            # setting certificate location information 

            if Port=="0":
                Command="echo -n Q | openssl x509 -noout -dates < "+Adress
                # setting up a check for the date of the local certificate
            else:
                Command=" echo -n Q | openssl s_client -servername "+Adress+" -connect "+Adress+":"+Port+" | openssl x509 -noout -dates"
                # setting up a check for the date of the remote certificate

            Output=subprocess.getoutput(Command)
            Tab=Output.split("\n")
            # execution of the check

            for Item in Tab:
                Date=Pattern.match(Item)
                # searching for information on the certificate expiry date

            try:
                DateStr=Date.group(0).split("=")
                EndDate=str(DateStr[1].replace(" GMT","").replace(" ","-"))
                CertDate=datetime.strptime(EndDate,"%b-%d-%H:%M:%S-%Y")
                # convert certificate expiry date into datetime form

                Time=CertDate-NowDate
                # calculation of how much time remains until the certificate expires

                if StampDate>Time:
                    Mesage=Adress+" certyficate end after "+datetime.strftime(CertDate,"%d.%m.%Y %H:%M:%S")+", has been "+str(Time)
                    FinalMesage.append(Mesage)
                    print('['+datetime.strftime(CertDate,"%d/%b/%Y %H:%M:%S")+'] "'+Mesage+'"')
                    # Checking time is below the significance threshold

            except:
                FinalMesage.append("Problem with the line "+str(Counter))
                print('['+datetime.strftime(NowDate,"%d/%b/%Y %H:%M:%S")+'] "Problem with the line '+str(Counter)+'"')
                # returning a reading error for a particular certificate

            Counter+=1

    except:
        FinalMesage.append("File "+Config["InputFile"]+" cannot be opened")
        print('['+datetime.strftime(NowDate,"%d/%b/%Y %H:%M:%S")+'] "File '+Config["InputFile"]+' cannot be opened"')
    # checking whether the file with the certificate locations
    # has been successfully opened

    saveFile(Config["OutputFile"],FinalMesage,NowDate)
    # saving the result file

#################################################################

if __name__=="__main__":
    main()
