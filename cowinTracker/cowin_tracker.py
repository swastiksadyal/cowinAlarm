import time
import os
import sys
from cowin_api import CoWinAPI
import multiprocessing
from prettytable import PrettyTable
from playsound import playsound
import colorama
cowin = CoWinAPI()
states = cowin.get_states()
print("""^ ^
(O,O)
(   ) Cowin Alarm
-"-"-----------------""")

def checkForDoses(ID,age_lim):
    for j in range(len(_centers["centers"][ID]["sessions"])):
        if(int(_centers["centers"][ID]["sessions"][j]["available_capacity"]) > 1):
            if(int(_centers["centers"][ID]["sessions"][j]["min_age_limit"]) == age_lim):
                return True

def playSound():
    p = multiprocessing.Process(target=playsound, args=("./alarmSound/alarm-sound-effect.mp3",))
    p.start()
    input("press ENTER to stop playback")
    p.terminate()

def updateData(dist,center):
    _centers = cowin.get_availability_by_district(dist)
    centerID_Index = -1
    for a in range(len(_centers["centers"])):
        if(int(_centers["centers"][a]["center_id"]) == center):
            centerID_Index = a
    return centerID_Index

def what():
    Y = input("Y/N")
    if(Y == "Y") or (Y == "y") or (Y == 'yes') or (Y == 1):
        return True
    else:
        return False

colorama.init()
path = "use_data.txt"
isFile = os.path.isfile(path)

if(isFile):
    size = os.path.getsize(path)
    with open('use_data.txt') as data:
        #print(data.readlines())
        data_ = list(data)
        print("\033[1;33;40m Please check Your Information...(Based upon the last Search you did)  \033[1;33;40m")
        for a in range(len(data_)):
            print(data_[a])
        print(" \033[1;33;40m Do you want to search for the same ?")
    if(what()):
        #none
        #none
        s1 = data_[1]
        state = [x for x in s1.split() if x.isdigit() == True]
        state = state[0]
        s2 = data_[2]
        dist = [x for x in s2.split() if x.isdigit() == True]
        district = dist[0]
        s3 = data_[3]
        center = [x for x in s3.split() if x.isdigit() == True]
        center = center[0]
        _centers = cowin.get_availability_by_district(district)
        availability = []
        availableAt = []
        print("\033[2;37;40m All the Centers in the District ...")
        Ctable = PrettyTable(["Center ID", "Name", "Pincode", "Fee","Block","Session"])
        for iD in range(len(_centers["centers"])):
            sessTable = PrettyTable(["Date","Available Capacity","Vaccine"])
            for j in range(len(_centers["centers"][iD]["sessions"])):
                sessTable.add_row([_centers["centers"][iD]["sessions"][j]["date"],_centers["centers"][iD]["sessions"][j]["available_capacity"],_centers["centers"][iD]["sessions"][j]["vaccine"]])
                if(int(_centers["centers"][iD]["sessions"][j]["available_capacity"]) > 1):
                    availability.append(int(_centers["centers"][iD]["sessions"][j]["available_capacity"]))
                    availableAt.append(_centers["centers"][iD]["center_id"])
            Ctable.add_row([_centers["centers"][iD]["center_id"],_centers["centers"][iD]["name"],_centers["centers"][iD]["pincode"],_centers["centers"][iD]["fee_type"],_centers["centers"][iD]["block_name"],sessTable])
      
        time.sleep(2)
        print(Ctable)
        centerID = int(center)
        centerID_Index = 0
        print("Your Center Info!")
        time.sleep(2)
        for a in range(len(_centers["centers"])):
            if(int(_centers["centers"][a]["center_id"]) == centerID):
                centerID_Index = a
        center_Info = PrettyTable([" ", "   ","    "])
        center_Info.add_row(["Center ID",int(_centers["centers"][centerID_Index]["center_id"]),_centers["centers"][centerID_Index]["name"]])
        center_Info.add_row(["---------","---------","---------"])
        center_Info.add_row(["Address ",_centers["centers"][centerID_Index]["address"],_centers["centers"][centerID_Index]["pincode"]])
        center_Info.add_row(["---------","---------","---------"])
        center_Info.add_row([" ",_centers["centers"][centerID_Index]["block_name"],_centers["centers"][centerID_Index]["district_name"]])
        center_Info.add_row(["---------","---------","---------"])
        center_Info.add_row(["Fee Type ",_centers["centers"][centerID_Index]["fee_type"]," "])
        center_Info.add_row(["---------","---------","---------"])
        center_Info.add_row(["Time",_centers["centers"][centerID_Index]["from"],_centers["centers"][centerID_Index]["to"]])
        center_Info.add_row(["---------","---------","---------"])
        center_Info.add_row(["Session","---------","---------"])
        center_Info.add_row(["---------","---------","---------"])
        for j in range(len(_centers["centers"][centerID_Index]["sessions"])):
            center_Info.add_row(["Date",_centers["centers"][centerID_Index]["sessions"][j]["date"]," "])
            center_Info.add_row(["---------","---------","---------"])
            center_Info.add_row(["Session ID",_centers["centers"][centerID_Index]["sessions"][j]["session_id"]," "])
            center_Info.add_row(["---------","---------","---------"])
            center_Info.add_row(["Available",_centers["centers"][centerID_Index]["sessions"][j]["available_capacity"]," "])
            center_Info.add_row(["---------","---------","---------"])
            center_Info.add_row(["Min Age",_centers["centers"][centerID_Index]["sessions"][j]["min_age_limit"]," "])
            center_Info.add_row(["---------","---------","---------"])
            center_Info.add_row(["Vaccine",_centers["centers"][centerID_Index]["sessions"][j]["vaccine"]," "])
            center_Info.add_row(["---------","---------","---------"])
            center_Info.add_row(["Dose 1",_centers["centers"][centerID_Index]["sessions"][j]["available_capacity_dose1"]," "])
            center_Info.add_row(["---------","---------","---------"])
            center_Info.add_row(["Dose 2",_centers["centers"][centerID_Index]["sessions"][j]["available_capacity_dose2"]," "])
    
        print(center_Info)
        print("\033[2;37;40m Your Center : \033[0;37;40m")
        #data.write(str(_centers["centers"][centerID_Index]["center_id"]) + " " + str(_centers["centers"][centerID_Index]["name"]) + "\n")
        print(str(_centers["centers"][centerID_Index]["center_id"]) + " " + str(_centers["centers"][centerID_Index]["name"]))
    else:
        os.remove(path)
       # os.execl(sys.executable, os.path.abspath("cowin_tracker.py"), *sys.argv)
        os.system('python "cowin_tracker.py"')
        #if (size < 1):
           # os.remove(path)
            #fileSys()
else:
    data = open(path,"w")
    data.write("1 \n")
    #data.close()
    state_table = PrettyTable(["State ID","State Name"])
    for i in range(len(states["states"])):
        state_table.add_row([(states["states"][i]["state_id"]),(states["states"][i]["state_name"])])
    print("\033[0;37;48m Find Your State here!")
    print(state_table)
    state = input("Enter Your State ID: ")
    state_index = -1
    for i in range(len(states["states"])):
        if(int(states["states"][i]["state_id"]) == int(state)):
            state_index = i
    data.write(state + " " + states["states"][state_index]["state_name"] + "\n")
    print(state + " " + states["states"][state_index]["state_name"])
    dist = cowin.get_districts(state)
    print("\033[0;37;48m Find your District here!")
    print("district ID +++++++++ District Name")
    print("---------------------------------")
    for i in range(len(dist["districts"])):
        print(str(dist["districts"][i]["district_id"]) + "             ||    "+ str(dist["districts"][i]["district_name"]))
    district = input("Enter your district ID: ")
    dist_index = -1
    for i in range(len(dist["districts"])):
        if(int(dist["districts"][i]["district_id"]) == int(district)):
            dist_index = i
    data.write(district + " " + dist["districts"][dist_index]["district_name"] + "\n")
    print(district + " " + dist["districts"][dist_index]["district_name"])
    _centers = cowin.get_availability_by_district(district)
    availability = []
    availableAt = []
    Ctable = PrettyTable(["Center ID", "Name", "Pincode", "Fee","Block","Session"])
    for iD in range(len(_centers["centers"])):
        sessTable = PrettyTable(["Date","Available Capacity","Vaccine"])
        for j in range(len(_centers["centers"][iD]["sessions"])):
            sessTable.add_row([_centers["centers"][iD]["sessions"][j]["date"],_centers["centers"][iD]["sessions"][j]["available_capacity"],_centers["centers"][iD]["sessions"][j]["vaccine"]])
            if(int(_centers["centers"][iD]["sessions"][j]["available_capacity"]) > 1):
                availability.append(int(_centers["centers"][iD]["sessions"][j]["available_capacity"]))
                availableAt.append(_centers["centers"][iD]["center_id"])
        Ctable.add_row([_centers["centers"][iD]["center_id"],_centers["centers"][iD]["name"],_centers["centers"][iD]["pincode"],_centers["centers"][iD]["fee_type"],_centers["centers"][iD]["block_name"],sessTable])
    print(Ctable)
    centerID = int(input("Enter the center ID you want to follow: "))
    centerID_Index = 0
    for a in range(len(_centers["centers"])):
        if(int(_centers["centers"][a]["center_id"]) == centerID):
            centerID_Index = a
     #       print(_centers["centers"][a])
    #print(centerID_Index)
    #print(_centers["centers"][centerID_Index])
    center_Info = PrettyTable([" ", "   ","    "])
    center_Info.add_row(["Center ID",int(_centers["centers"][centerID_Index]["center_id"]),_centers["centers"][centerID_Index]["name"]])
    center_Info.add_row(["---------","---------","---------"])
    center_Info.add_row(["Address ",_centers["centers"][centerID_Index]["address"],_centers["centers"][centerID_Index]["pincode"]])
    center_Info.add_row(["---------","---------","---------"])
    center_Info.add_row([" ",_centers["centers"][centerID_Index]["block_name"],_centers["centers"][centerID_Index]["district_name"]])
    center_Info.add_row(["---------","---------","---------"])
    center_Info.add_row(["Fee Type ",_centers["centers"][centerID_Index]["fee_type"]," "])
    center_Info.add_row(["---------","---------","---------"])
    center_Info.add_row(["Time",_centers["centers"][centerID_Index]["from"],_centers["centers"][centerID_Index]["to"]])
    center_Info.add_row(["---------","---------","---------"])
    center_Info.add_row(["Session","---------","---------"])
    center_Info.add_row(["---------","---------","---------"])
    for j in range(len(_centers["centers"][centerID_Index]["sessions"])):
        center_Info.add_row(["Date",_centers["centers"][centerID_Index]["sessions"][j]["date"]," "])
        center_Info.add_row(["---------","---------","---------"])
        center_Info.add_row(["Session ID",_centers["centers"][centerID_Index]["sessions"][j]["session_id"]," "])
        center_Info.add_row(["---------","---------","---------"])
        center_Info.add_row(["Available",_centers["centers"][centerID_Index]["sessions"][j]["available_capacity"]," "])
        center_Info.add_row(["---------","---------","---------"])
        center_Info.add_row(["Min Age",_centers["centers"][centerID_Index]["sessions"][j]["min_age_limit"]," "])
        center_Info.add_row(["---------","---------","---------"])
        center_Info.add_row(["Vaccine",_centers["centers"][centerID_Index]["sessions"][j]["vaccine"]," "])
        center_Info.add_row(["---------","---------","---------"])
        center_Info.add_row(["Dose 1",_centers["centers"][centerID_Index]["sessions"][j]["available_capacity_dose1"]," "])
        center_Info.add_row(["---------","---------","---------"])
        center_Info.add_row(["Dose 2",_centers["centers"][centerID_Index]["sessions"][j]["available_capacity_dose2"]," "])
    print("\033[1;32;40m Here IS your Center:")
    print(center_Info)
    data.write(str(_centers["centers"][centerID_Index]["center_id"]) + " " + str(_centers["centers"][centerID_Index]["name"]) + "\n")
    print(str(_centers["centers"][centerID_Index]["center_id"]) + " " + str(_centers["centers"][centerID_Index]["name"]))
    # the main program starts here
    age = int(input("Enter your age: "))
    if(age < 45):
        age_lim = 18
    else:
        age_lim = 45
    data.close()

age = int(input("Enter your age: "))
if(age < 45):
    age_lim = 18
else:
    age_lim = 45
input("press ENTER to begin search...")
ID = updateData(district,centerID)

if(checkForDoses(ID,age_lim)):
    print("\033[1;32;40m Woohoo! vaccine is available... register fast")
else:
    print("\033[1;31;40m I`m sorry I couldn`t find any available vaccine Slots \n If you want i can keep on looking and will notify when any slot is available!")
    if(what()):
        print("\033[1;31;40m I`ll keep on looking... please don`t turn off the script or your compute machine if possible")
        while(checkForDoses(ID,age_lim) != False):
            if(checkForDoses(ID,age_lim)):
                print("\033[0;32;47m Well done Slot has been found TaDa!")
                playSound()
                break
            else:
                ID = updateData(district,centerID)
                print(".",end ="")
            time.sleep(30)
        print("Thank you!")
    else:
        print("\033[0;36;47m Thank You! \n Try again some time later maybe you`ll get lucky")
# Created with <3 by Swastik @swastiksadyal
# please be noted that this script might contain bug and you are on your own if you find any
# or you can let me know by pinging
# created in 3 Hours in total 
