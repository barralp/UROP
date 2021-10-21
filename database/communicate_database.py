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
    mydb = mysql.connector.connection.MySQLConnection(host = 
        'localhost', user = 'root', password = 'DFLVXdq4$',
        database = 'imagesdypoledatabase')
    #mydb = mysql.connector.connect(host = 'localhost',
     #                   user = 'root',
      #                  password = 'DFLVXdq4$',
       #                 database = 'imagesdypoledatabase')
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

def getQuery(sql_query):
    listOut = executeGetQuery(sql_query)
    return np.array(listOut, dtype = np.float64)[:,0]

def getEntireColumn(variable, table):
    sql_query = """SELECT """ + variable + " FROM " + table + ";"
    return getQuery(sql_query)
    #put into dataframe where column name is variable

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
