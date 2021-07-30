# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 10:51:32 2020

@author: Pierre
"""

import numpy as np
import mysql.connector
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

MYSQLserverIP = "192.168.1.133"
username = "root"
password = "5buster13"
databaseName = "DFLVXdq4$"

#### Used functions ####
# change here the selection global / local
def setConnection(typeOfConnection = 'local'):
    if typeOfConnection == 'local':
        return setLocalConnection()
    elif typeOfConnection == 'global':
        return setDistantConnection()
    else:
        print('Set what type of connection you want')

def setLocalConnection():
    # Open database connection
    mydb = mysql.connector.connect(host = "localhost",
                        user = "5buster13",
                        password = "DFLVXdq4$",
                        database = "imagesdypoledatabase")
    #print('Local connection established')
    return mydb

def setDistantConnection():
    # Open database connection
    mydb = mysql.connector.connect(host = MYSQLserverIP,
                        user = username,
                        password = password,
                        database = databaseName)
    #print('Distant connection established')
    return mydb
    
def getLastImageID():
    sql_query = """SELECT imageID FROM images ORDER BY imageID DESC LIMIT 1;"""
    lastImageID = executeGetQuery(sql_query)[0][0]
    return lastImageID

def getRunIDFromImageID(imageID):
    sql_query = "SELECT runID_fk FROM images WHERE imageID = {} ;".format(imageID)
    runID_fk = executeGetQuery(sql_query)[0][0]
    return runID_fk
    
def getNCount(imageID):
    try:
        runID_fk = getRunIDFromImageID(imageID)
        sql_query = "SELECT nCount FROM nCounts WHERE runID_fk = {} ;".format(runID_fk)
        nCount = executeGetQuery(sql_query)[0][0]
    except:
        nCount = 0.0
    return nCount

def getVariable(g) :
    sql_query = "SELECT " + g + " FROM ciceroOut;"
    variable = executeGetQuery(sql_query)[0]
    return variable
    
def getRunID() :
    sql_query = "SELECT runID FROM ciceroOut;"
    runID = executeGetQuery(sql_query)[0]
    return runID

def getIterationNum() :
    sql_query = "SELECT IterationNum FROM ciceroOut;"
    iterationNum = executeGetQuery(sql_query)[0]
    return iterationNum

def getIterationCount() :
    sql_query = "SELECT IterationCount FROM ciceroOut;"
    iterationCount = executeGetQuery(sql_query)[0]
    return iterationCount

def getRunningCounter() :
    sql_query = "SELECT RunningCounter FROM ciceroOut;"
    runningCounter = executeGetQuery(sql_query)[0]
    return runningCounter

def getTOF() :
    sql_query = "SELECT TOF FROM ciceroOut;"
    TOF = executeGetQuery(sql_query)[0]
    return TOF

def getCompLevel() :
    sql_query = "SELECT CompLevel FROM ciceroOut;"
    compLevel = executeGetQuery(sql_query)[0]
    return compLevel

def getImgFreq() :
    sql_query = "SELECT ImgFreq FROM ciceroOut;"
    imgFreq = executeGetQuery(sql_query)[0]
    return imgFreq

def getDummy() :
    sql_query = "SELECT dummy FROM ciceroOut;"
    dummy = executeGetQuery(sql_query)[0]
    return dummy

def getIodineFreq() :
    sql_query = "SELECT IodineFreq FROM ciceroOut;"
    iodineFreq = executeGetQuery(sql_query)[0]
    return iodineFreq

def getFinalBField() :
    sql_query = "SELECT FinalBField FROM ciceroOut;"
    finalBField = executeGetQuery(sql_query)[0]
    return finalBField

def getCameraFudgeTime() :
    sql_query = "SELECT CameraFudgeTime FROM ciceroOut;"
    cameraFudgeTime = executeGetQuery(sql_query)[0]
    return cameraFudgeTime

def getLoadTime() :
    sql_query = "SELECT LoadTime FROM ciceroOut;"
    loadTime = executeGetQuery(sql_query)[0]
    return loadTime

def getCompTime() :
    sql_query = "SELECT CompTime FROM ciceroOut;"
    compTime = executeGetQuery(sql_query)[0]
    return compTime

def getLoadCurrent() :
    sql_query = "SELECT LoadCurrent FROM ciceroOut;"
    loadCurrent = executeGetQuery(sql_query)[0]
    return loadCurrent

def getTimeStamp() :
    sql_query = "SELECT timestamp FROM ciceroOut;"
    timestamp = executeGetQuery(sql_query)[0]
    return timestamp

def getWee() :
    sql_query = "SELECT wee FROM ciceroOut;"
    wee = executeGetQuery(sql_query)[0]
    return wee

def getMotLoadFreq() :
    sql_query = "SELECT MOTLoadFreq FROM ciceroOut;"
    MOTLoadFreq = executeGetQuery(sql_query)[0]
    return MOTLoadFreq

def getTime() :
    sql_query = "SELECT time FROM ciceroOut;"
    time = executeGetQuery(sql_query)[0]
    return time

def getZSPower() :
    sql_query = "SELECT ZSPower FROM ciceroOut;"
    ZSPower = executeGetQuery(sql_query)[0]
    return ZSPower

def getImageTime() :
    sql_query = "SELECT imageTime FROM ciceroOut;"
    imageTime = executeGetQuery(sql_query)[0]
    return imageTime

def getMOTLevel() :
    sql_query = "SELECT MOTLevel FROM ciceroOut;"
    MOTLevel = executeGetQuery(sql_query)[0]
    return MOTLevel

def getCompX() :
    sql_query = "SELECT compx FROM ciceroOut;"
    compX = executeGetQuery(sql_query)[0]
    return compX

def getCompY() :
    sql_query = "SELECT compy FROM ciceroOut;"
    compY = executeGetQuery(sql_query)[0]
    return compY

def getLossTime() :
    sql_query = "SELECT LossTime FROM ciceroOut;"
    lossTime = executeGetQuery(sql_query)[0]
    return lossTime

def getTCFreq() :
    sql_query = "SELECT TCFreq FROM ciceroOut;"
    TCFreq = executeGetQuery(sql_query)[0]
    return TCFreq

def getCompZ() :
    sql_query = "SELECT compz FROM ciceroOut;"
    compZ = executeGetQuery(sql_query)[0]
    return compZ

def getMOTCurrentAmps() :
    sql_query = "SELECT MOTCurrent_Amps FROM ciceroOut;"
    MOTCurrentAmps = executeGetQuery(sql_query)[0]
    return MOTCurrentAmps

def getMOTLoadCurrentAmps() :
    sql_query = "SELECT MOTLoadCurrent_Amps FROM ciceroOut;"
    MOTLoadCurrentAmps = executeGetQuery(sql_query)[0]
    return MOTLoadCurrentAmps

def getCompTime2() :
    sql_query = "SELECT CompTime2 FROM ciceroOut;"
    compTime2 = executeGetQuery(sql_query)[0]
    return compTime2

def getCompLevel2() : 
    sql_query = "SELECT CompLevel2 FROM ciceroOut;"
    compLevel2 = executeGetQuery(sql_query)[0]
    return compLevel2

def getMOTCompFreq() :
    sql_query = "SELECT MOTCompFreq FROM ciceroOut;"
    MOTCompFreq = executeGetQuery(sql_query)[0]
    return MOTCompFreq

def getMOTCompFreq2() :
    sql_query = "SELECT MOTCompFreq2 FROM ciceroOut;"
    MOTCompFreq2 = executeGetQuery(sql_query)[0]
    return MOTCompFreq2

def getFreqCompTime2() :
    sql_query = "SELECT FreqCompTime2 FROM ciceroOut;"
    freqCompTime2 = executeGetQuery(sql_query)[0]
    return freqCompTime2

def getFinalYComp() :
    sql_query = "SELECT FinalYComp FROM ciceroOut;"
    finalYComp = executeGetQuery(sql_query)[0]
    return finalYComp

def getCompHoldTime() :
    sql_query = "SELECT CompHoldTime FROM ciceroOut;"
    compHoldTime = executeGetQuery(sql_query)[0]
    return compHoldTime

def getWaitTime() :
    sql_query = "SELECT WaitTime FROM ciceroOut;"
    waitTime = executeGetQuery(sql_query)[0]
    return waitTime

def getASPower() :
    sql_query = "SELECT ASPower FROM ciceroOut;"
    ASPower = executeGetQuery(sql_query)[0]
    return ASPower

def getASPowermW() :
    sql_query = "SELECT ASPower_mW FROM ciceroOut;"
    ASPowermW = executeGetQuery(sql_query)[0]
    return ASPowermW

def getASPowermW2() :
    sql_query = "SELECT ASPower_mW_2 FROM ciceroOut;"
    ASPowermW2 = executeGetQuery(sql_query)[0]
    return ASPowermW2

def getMOTCurrent2() :
    sql_query = "SELECT MOTCurrent2 FROM ciceroOut;"
    MOTCurrent2 = executeGetQuery(sql_query)[0]
    return MOTCurrent2

def getLevel1() :
    sql_query = "SELECT level1 FROM ciceroOut;"
    level1 = executeGetQuery(sql_query)[0]
    return level1

def getLevel2() :
    sql_query = "SELECT level2 FROM ciceroOut;"
    level2 = executeGetQuery(sql_query)[0]
    return level2

def getLevel3() :
    sql_query = "SELECT level3 FROM ciceroOut;"
    level3 = executeGetQuery(sql_query)[0]
    return level3

def getLevel4() :
    sql_query = "SELECT level4 FROM ciceroOut;"
    level4 = executeGetQuery(sql_query)[0]
    return level4

def getLevel5() :
    sql_query = "SELECT level5 FROM ciceroOut;"
    level5 = executeGetQuery(sql_query)[0]
    return level5

def getFreq1() :
    sql_query = "SELECT freq1 FROM ciceroOut;"
    freq1 = executeGetQuery(sql_query)[0]
    return freq1

def getFreq2() :
    sql_query = "SELECT freq2 FROM ciceroOut;"
    freq2 = executeGetQuery(sql_query)[0]
    return freq2

def getFreq3() :
    sql_query = "SELECT freq3 FROM ciceroOut;"
    freq3 = executeGetQuery(sql_query)[0]
    return freq3

def getFreq4() :
    sql_query = "SELECT freq4 FROM ciceroOut;"
    freq4 = executeGetQuery(sql_query)[0]
    return freq4

def getFreq5() :
    sql_query = "SELECT freq5 FROM ciceroOut;"
    freq5 = executeGetQuery(sql_query)[0]
    return freq5

def getODTRamp() :
    sql_query = "SELECT ODT_Ramp FROM ciceroOut;"
    ODTRamp = executeGetQuery(sql_query)[0]
    return ODTRamp

def getODTHoldTime() :
    sql_query = "SELECT ODTHoldTime FROM ciceroOut;"
    ODTHoldTime = executeGetQuery(sql_query)[0]
    return ODTHoldTime

def getODT1Final() :
    sql_query = "SELECT ODT1_Final FROM ciceroOut;"
    ODT1Final = executeGetQuery(sql_query)[0]
    return ODT1Final

def getODT2Final() :
    sql_query = "SELECT ODT2_Final FROM ciceroOut;"
    ODT2Final = executeGetQuery(sql_query)[0]
    return ODT2Final

def getEvapTime2() :
    sql_query = "SELECT EvapTime2 FROM ciceroOut;"
    evapTime2 = executeGetQuery(sql_query)[0][0]
    return evapTime2

def getEvapTime1() :
    sql_query = "SELECT EvapTime1 FROM ciceroOut;"
    evapTime1 = executeGetQuery(sql_query)[0]
    return evapTime1

def getEvapTime3() :
    sql_query = "SELECT EvapTime3 FROM ciceroOut;"
    evapTime3 = executeGetQuery(sql_query)[0]
    return evapTime3

def getBigZ() :
    sql_query = "SELECT BigZ FROM ciceroOut;"
    bigZ = executeGetQuery(sql_query)[0]
    return bigZ

def getSGOn() :
    sql_query = "SELECT SGOn FROM ciceroOut;"
    SGOn = executeGetQuery(sql_query)[0]
    return SGOn

def getSGOn2() :
    sql_query = "SELECT SGOn2 FROM ciceroOut;"
    SGOn2 = executeGetQuery(sql_query)[0]
    return SGOn2

def getPumpTime() :
    sql_query = "SELECT PumpTime FROM ciceroOut;"
    pumpTime = executeGetQuery(sql_query)[0]
    return pumpTime

def getDopplerCoolFreq() :
    sql_query = "SELECT DopplerCoolFreq FROM ciceroOut;"
    dopplerCoolFreq = executeGetQuery(sql_query)[0]
    return dopplerCoolFreq

def getODT1Init() :
    sql_query = "SELECT ODT1_Init FROM ciceroOut;"
    ODT1Init = executeGetQuery(sql_query)[0]
    return ODT1Init

def getODT1Evap1End() :
    sql_query = "SELECT ODT1_Evap1_End FROM ciceroOut;"
    ODT1Evap1End = executeGetQuery(sql_query)[0]
    return ODT1Evap1End

def getODT2Init() :
    sql_query = "SELECT ODT2_Init FROM ciceroOut;"
    ODT2Init = executeGetQuery(sql_query)[0]
    return ODT2Init

def getODT2Evap1End() :
    sql_query = "SELECT ODT2_Evap1_End FROM ciceroOut;"
    ODT2Evap1Init = executeGetQuery(sql_query)[0]
    return ODT2Evap1Init

def getFeshbachCurrent() :
    sql_query = "SELECT FeshbachCurrent FROM ciceroOut;"
    feshbachCurrent = executeGetQuery(sql_query)[0]
    return feshbachCurrent

def getEvapTime4() :
    sql_query = "SELECT EvapTime4 FROM ciceroOut;"
    evapTime4 = executeGetQuery(sql_query)[0]
    return evapTime4

def getAMFreq() :
    sql_query = "SELECT AMFreq FROM ciceroOut;"
    AMFreq = executeGetQuery(sql_query)[0]
    return AMFreq

def getAMDuration() :
    sql_query = "SELECT AMDuration FROM ciceroOut;"
    AMDuration = executeGetQuery(sql_query)[0]
    return AMDuration

def getODTRampUp() :
    sql_query = "SELECT ODTRampUp FROM ciceroOut;"
    ODTRampUp = executeGetQuery(sql_query)[0]
    return ODTRampUp

def getEvap2Factor() :
    sql_query = "SELECT Evap2Factor FROM ciceroOut;"
    evap2Factor = executeGetQuery(sql_query)[0]
    return evap2Factor

def getTau() :
    sql_query = "SELECT tau FROM ciceroOut;"
    tau = executeGetQuery(sql_query)[0]
    return tau

def getTotalExp() :
    sql_query = "SELECT totalExp FROM ciceroOut;"
    totalExp = executeGetQuery(sql_query)[0]
    return totalExp

def getInTrapCoolFreq() :
    sql_query = "SELECT InTrapCoolFreq FROM ciceroOut;"
    inTrapCoolFreq = executeGetQuery(sql_query)[0]
    return inTrapCoolFreq

def getInTrapCoolTime() :
    sql_query = "SELECT InTrapCoolTime FROM ciceroOut;"
    inTrapCoolTime = executeGetQuery(sql_query)[0]
    return inTrapCoolTime

def getEvapTime5() :
    sql_query = "SELECT EvapTime5 FROM ciceroOut;"
    evapTime5 = executeGetQuery(sql_query)[0]
    return evapTime5

def getEvap1EndGradient() :
    sql_query = "SELECT Evap1_End_Gradient FROM ciceroOut;"
    evap1EndGradient = executeGetQuery(sql_query)[0]
    return evap1EndGradient

def getVar60() :
    sql_query = "SELECT Var60 FROM ciceroOut;"
    var60 = executeGetQuery(sql_query)[0]
    return var60

def getEvapScan() :
    sql_query = "SELECT EvapScan FROM ciceroOut;"
    evapScan = executeGetQuery(sql_query)[0]
    return evapScan

def getEvapGradientInit() :
    sql_query = "SELECT Evap_Gradient_Init FROM ciceroOut;"
    evapGradientInit = executeGetQuery(sql_query)[0]
    return evapGradientInit

def getEvapGradient1() :
    sql_query = "SELECT Evap_Gradient1 FROM ciceroOut;"
    evapGradient1 = executeGetQuery(sql_query)[0]
    return evapGradient1

def getEvapGradient2() :
    sql_query = "SELECT Evap_Gradient2 FROM ciceroOut;"
    evapGradient2 = executeGetQuery(sql_query)[0]
    return evapGradient2

def getEvapGradient3() :
    sql_query = "SELECT Evap_Gradient3 FROM ciceroOut;"
    evapGradient3 = executeGetQuery(sql_query)[0]
    return evapGradient3

def getEvapEndGradient() :
    sql_query = "SELECT Evap_End_Gradient FROM ciceroOut;"
    evapEndGradient = executeGetQuery(sql_query)[0]
    return evapEndGradient

def getODTTOFGradient() :
    sql_query = "SELECT ODT_TOF_Gradient FROM ciceroOut;"
    ODTTOFGradient = executeGetQuery(sql_query)[0]
    return ODTTOFGradient

def getODTTOFBigZ() :
    sql_query = "SELECT ODT_TOF_BigZ FROM ciceroOut;"
    ODTTOFBigZ = executeGetQuery(sql_query)[0]
    return ODTTOFBigZ

def getEvap5BigZ() :
    sql_query = "SELECT Evap5_BigZ FROM ciceroOut;"
    evap5BigZ = executeGetQuery(sql_query)[0]
    return evap5BigZ

def getFinalODT1() :
    sql_query = "SELECT FinalODT1 FROM ciceroOut;"
    finalODT1 = executeGetQuery(sql_query)[0]
    return finalODT1

def getBlinckingTime() :
    sql_query = "SELECT BlinckingTime FROM ciceroOut;"
    blinckingTime = executeGetQuery(sql_query)[0]
    return blinckingTime

def getBlinckingFreq() :
    sql_query = "SELECT Blincking_freq FROM ciceroOut;"
    blinckingFreq = executeGetQuery(sql_query)[0]
    return blinckingFreq

def getMolassesLevel() :
    sql_query = "SELECT Molasses_level FROM ciceroOut;"
    molassesLevel = executeGetQuery(sql_query)[0]
    return molassesLevel

def getBlinckingDuration() :
    sql_query = "SELECT Blincking_Duration FROM ciceroOut;"
    blinckingDuration = executeGetQuery(sql_query)[0]
    return blinckingDuration

def getODTMolasses() :
    sql_query = "SELECT ODT_Molasses FROM ciceroOut;"
    ODTMolasses = executeGetQuery(sql_query)[0]
    return ODTMolasses

def getODTMolassesZField() :
    sql_query = "SELECT ODT_Molasses_ZField FROM ciceroOut;"
    ODTMolassesZField = executeGetQuery(sql_query)[0]
    return ODTMolassesZField

def getODTLoad_MOT_Freq() :
    sql_query = "SELECT ODTLoad_MOT_Freq FROM ciceroOut;"
    ODTLoadMOTFreq = executeGetQuery(sql_query)[0]
    return ODTLoadMOTFreq

def getODTCompX() :
    sql_query = "SELECT ODTCompx FROM ciceroOut;"
    ODTCompX = executeGetQuery(sql_query)[0]
    return ODTCompX

def getODTCompY() :
    sql_query = "SELECT ODTCompy FROM ciceroOut;"
    ODTCompY = executeGetQuery(sql_query)[0]
    return ODTCompY

def getODTCompZ() :
    sql_query = "SELECT ODTCompz FROM ciceroOut;"
    ODTCompZ = executeGetQuery(sql_query)[0]
    return ODTCompZ

def getBlinckingLength() :
    sql_query = "SELECT Blinckinglength FROM ciceroOut;"
    blinckingLength = executeGetQuery(sql_query)[0]
    return blinckingLength

def getODTLoad_MOTFreq() :
    sql_query = "SELECT ODTLoad_MOTFreq FROM ciceroOut;"
    ODTLoadMOTFreq = executeGetQuery(sql_query)[0]
    return ODTLoadMOTFreq

def getEvap1CompZ() :
    sql_query = "SELECT Evap1_CompZ FROM ciceroOut;"
    evap1CompZ = executeGetQuery(sql_query)[0]
    return evap1CompZ

def getPumpingFreq() :
    sql_query = "SELECT Pumping_Freq FROM ciceroOut;"
    pumpingFreq = executeGetQuery(sql_query)[0]
    return pumpingFreq

def getCompXEarth() :
    sql_query = "SELECT compx_Earth FROM ciceroOut;"
    compXEarth = executeGetQuery(sql_query)[0]
    return compXEarth

def getCompYEarth() :
    sql_query = "SELECT compy_Earth FROM ciceroOut;"
    compYEarth = executeGetQuery(sql_query)[0]
    return compYEarth

def getCompZEarth() :
    sql_query = "SELECT compz_Earth FROM ciceroOut;"
    compZEarth = executeGetQuery(sql_query)[0]
    return compZEarth

def getEvapTime6() :
    sql_query = "SELECT EvapTime6 FROM ciceroOut;"
    evapTime6 = executeGetQuery(sql_query)[0]
    return evapTime6

def getCompZ2() :
    sql_query = "SELECT compz2 FROM ciceroOut;"
    compZ2 = executeGetQuery(sql_query)[0]
    return compZ2


def executeGetQuery(sql_query): # works when you don't need to use db.commit, so for read only functions
    db = setConnection()
    cursor = db.cursor()
    cursor.execute(sql_query)
    cursorResult = cursor.fetchall()
    cursor.close()
    db.close()
    return cursorResult

#lastImageID = getLastImageID()
#lastRunID = getRunIDFromImageID(lastImageID)
#setLocalConnection()
#print(lastImageID)
#print(lastRunID)
#print(getNCount(lastImageID))

#### Unused functions ####
"""
def dataToArray(pathFile):
    # Convert camera fits data to binary format
    with open(pathFile, 'rb') as file:
        image = fits.getdata(file)
    return image[0].ravel().tolist(), image[1].ravel().tolist(), image[2].ravel().tolist()   # atoms, noAtoms, dark

def getTimestamp(imageID):
    sql_query = "SELECT timestamp FROM images WHERE imageID = " + str(imageID) + ";"
    timestamp = executeGetQuery(sql_query)[0][0]
    return timestamp

def getLastImageIDs(n):
    sql_query = "SELECT imageID FROM images ORDER BY imageID DESC LIMIT " + str(n) + ";"
    lastImageIDsTupleList = executeGetQuery(sql_query)
    lastImageIDs = listTupleToList(lastImageIDsTupleList)
    return lastImageIDs

def listTupleToList(List):
    outputList = []
    for oneTuple in List:
        outputList += [oneTuple[0]]
    return outputList
"""
