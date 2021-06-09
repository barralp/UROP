import numpy as np
import mysql.connector
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

class DataParser(fileName, runID) : 
    def __init__(self):
        m_fileName = open(fileName)
        m_runID = runID

    def getTOF() :
        sql_query = "SELECT TOF FROM ciceroOut ORDER BY m_runID;"
        TOF = executeGetQuery(sql_query)[0][0]
        return TOF

    def getLoadCurrent() :
        sql_query = "SELECT LoadCurrent FROM ciceroOut ORDER BY m_runID;"
        LoadCurrent = executeGetQuery(sql_query)[0][0]
        return LoadCurrent

