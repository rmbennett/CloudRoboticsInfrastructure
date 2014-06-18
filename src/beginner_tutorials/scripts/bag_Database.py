#!/usr/bin/env python
import shelve
import os
import rospkg
from datetime import datetime
import pywapi
import string


def openDatabase(file_path):   
	global bagDatabase
	path = os.path.join(rospkg.get_ros_home(), file_path)
	bagDatabase = shelve.open(path, flag = 'c', writeback = True)

def addNewBag(file):
	global bagDatabase
	#userId = getNumberOfBags() + 1
	userId = file
	bagDatabase[str(userId)] = {"FileName": '', "Topic": ''}
	bagDatabase.sync()
	return userId

#***************Getters****************

def getNumberOfBags():
	global bagDatabase
	return len(bagDatabase)

def bagExists(userId):
	global bagDatabase
	if str(userId) in bagDatabase.keys():
		return True
	else:
		return False

def getUserIds():
	global bagDatabase
	return bagDatabase.keys()

def getTopics(userId):
	global bagDatabase
	try:
		return bagDatabase[str(userId)]["Topic"]
	except:
		return "ERRORS"

def getFileName(userId):
	global bagDatabase
	try:
		return bagDatabase[str(userId)]["FileName"]
	except:	
		return ""

#*******************Setters**********************

def setFileName(userId, FileName):
	global bagDatabasef
	bagDatabase[str(userId)]["FileName"] = FileName
	bagDatabase.sync()


def setTopics(userId, Topic):
	global bagDatabase
	bagDatabase[str(userId)]["Topic"] = Topic
	bagDatabase.sync()

def ClearDatabase():
	global bagDatabase
	bagDatabase.clear() 
	bagDatabase.sync()

def CloseDatabase(file_path):
	global bagDatabase
	numberUsers = getNumberOfBags()
	try:
		bagDatabase.close()
		if numberUsers == 0:
			os.remove(os.path.join(rospkg.get_ros_home(), file_path))
	except Exception, e:
		print e



if __name__ == '__main__':
	# Main contains test code to test functionality. 
	DbTest = 'DbTest.db'
	openDatabase(DbTest)
	print "Get number of users should be 0"
	print getNumberOfBags()
	print "Check user 1 exists - should be false"
	print bagExists(1)
	UId = addNewBag("banter.bag")
	print "New user ID should be banter.bag"
	print UId
	print "Check User 1 exists should be true"
	print bagExists(UId)	
	print "Filename name - should be blank"
	print getFileName(UId)
	print "getNumberOfBags - should be 1"
	print getNumberOfBags()
	print "Set and Get Filename"
	setFileName(UId, 'Frederico.bag')
	print getFileName(UId)
	print "Set and Get Topic"
	setTopics(UId, 'Electronic and Infomation Engineering')
	print getTopics(UId)
	



	CloseDatabase(DbTest)
	openDatabase(DbTest)
	print getNumberOfBags()
	ClearDatabase()
	print getNumberOfBags()
	CloseDatabase(DbTest)