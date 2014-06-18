#!/usr/bin/python
import rospy
import cv2
import mongoLABhelper
import pymongo
import datetime

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
AlertCollection = mongoLABhelper.startAlertDatabaseURI("AlertCollection", "URI")
MotionCollection = mongoLABhelper.startMotionDatabaseURI("MotionCollection", "URI")
print AlertCollection
date = datetime.datetime.utcnow()
print date

def AlertSaveImage(AlertCollection, MotionCollection, date, frame):
	if mongoLABhelper.alertQuery(AlertCollection, date) == True:
		ImageName = "AlertMotionDetected"+datetime.datetime.now().strftime("%b %d, %H:%M:%S")+".jpg"
		cv2.imwrite(ImageName, frame)
		motion_id = mongoLABhelper.addMotionData(MotionCollection, ImageName, ImageName)
		print "Saved Image from second angle"

	return datetime.datetime.utcnow()

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False


while rval:
    #mongoLABhelper.addAlertData(AlertCollection, "Some banterous alert data")
    rval, frame = vc.read()
    cv2.imshow("preview", frame)
    date = AlertSaveImage(AlertCollection, MotionCollection, date, frame)
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")

