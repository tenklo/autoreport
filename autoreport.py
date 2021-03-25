#!/bin/python3
import webuntis
import datetime
import json


username = ""
password = ""

def getschooldatafor(monday):
    # TODO: actually get correct data, maybe even with the additional information
    friday = monday + datetime.timedelta(days=4)
    print("getting subjects from " + str(monday) + " to " + str(friday))

    session = webuntis.Session(
        server='mese.webuntis.com',
        username=username ,
        password=password ,
        school='IT-Schule Stuttgart',
        useragent='UserAgent'
    )

    session.login()
    index = 0

    klasse = session.klassen().filter(name="E2FI5")[0]
    tt = session.timetable(klasse=klasse, start=monday, end=friday)

    # for element in tt:
    #     print(element.subjects)
    subjectsthisweek = {}

    for element in tt:
        subj = str(element.subjects) + ": "
        subj = subj.replace('[', '')
        subj = subj.replace(']', '')

        if subj in subjectsthisweek and element.code != "cancelled":
            subjectsthisweek[subj][0] += 1
        elif element.code != "cancelled":
            subjectsthisweek[subj] = [ 0, "" ]

    for subj in subjectsthisweek:
        subjectsthisweek[subj][0] *= 2

    session.logout()
    return subjectsthisweek

def getworkdatafor(monday):
    print ("getting work data\nwork data is empty by default. write custom solution to include in autogeneration")
    return {"": ["", ""]}

def getsonstigesdatafor(monday):
    print ("getting sonstiges data\nsonstiges data is empty by default. write custom solution to include in autogeneration")
    return {"": ["", ""]}

def writetofile(filename, content):
    print("writing data to file " + filename)
    with open(filename, "w") as file:
        file.write(content)
def makeberichtsheftcontent(mondayofweek):
    berichtsheft = {
        "school": getschooldatafor(mondayofweek),
        "work" : getworkdatafor(mondayofweek),
        "sonstiges" : getsonstigesdatafor(mondayofweek)
    }
    return berichtsheft

def getmondayfordate(date):
    monday = date - datetime.timedelta(days=date.weekday())
    return monday
def createberichtsheftdatafor(date,filename):
    monday = getmondayfordate(date)

    berichtsheft = makeberichtsheftcontent(monday)
    jsonberichtsheft = json.dumps(berichtsheft, indent=4)

    writetofile(filename, jsonberichtsheft)

def createberichtsheftfor(date, filename):
    print("creating berichtsheft at " + filename)
    createtmpberichtsheft()
    modifytmpberichtsheft()
    finalizeberichtsheft()

def finalizeberichtsheft():
    pass
def rezipberichtsheft():
    pass

def createtmpberichtsheft():
    pass

def modifytmpberichtsheft():
    pass

def getconfig():
    # TODO: read from configfile/let user enter config
    # best to autoload if file exist, otherwise prompt
    config={
        "suffix": "_Ausbildung_Karsten_Kloess.odt",
        "name": "Karsten Klöss",
        "year": "2/3",
        "outputpath": "./hefte/",
        "template": "./.template.odt"
    }
    return config

def getpraefixfrom(date):
    return str(getmondayfordate(date)).replace("-", "")


# TODO: some way to specify the date, e.g. by argument or asking the user
date = datetime.date.today()
date = datetime.datetime.strptime("25.03.21", '%d.%m.%y').date()

config = getconfig()

berichtsheftdatafilename = getpraefixfrom(date) + ".json"
berichtsheftfilename = getpraefixfrom(date) + config["suffix"]
createberichtsheftdatafor(date, berichtsheftdatafilename)
createberichtsheftfor(date, berichtsheftfilename)
