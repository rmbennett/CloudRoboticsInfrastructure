#!/usr/bin/env python

import rospy
import rosbag
import subprocess
import yaml
import time
import os
import signal
import sys
import getopt
import tf
from std_msgs.msg import Int32, String
from p2os_driver.msg import SonarArray
from p2os_driver.msg import MotorState
import mongoLABhelper
import pymongo

def bump_callback(data):
    #bump_record(data) // for rosBag recording
    bump_mongo_record(data)


def bump_mongo_record(data):
    global bumpCollection

    bump_id = mongoLABhelper.addBumpData(bumpCollection, data.state)
    

def bump_record(data):
    global count_bump
    global count
    global t
    global recordedBump
    #print ("Motor State Value : %s " % (data.state))
    if(data.state == 0 and count == 0):    

        count= count + 1 
        rospy.loginfo(rospy.get_caller_id()+"Start Recording! BUMP")
        global procMessage
        t = time.time() 
        recordedBump = True
        procMessage = subprocess.Popen(["rosbag", "record", "-a","-o", "BumpBag"], preexec_fn=os.setsid)
        #time.sleep(10)
    
    elif(data.state == 0 and not count == 0 and not count == 10):
         count = count + 1

    elif(count == 10):
        count = 0
    
    elif((time.time() - t) >= 10 and recordedBump == True):
        t = 0
        recordedBump = False 
        rospy.loginfo(rospy.get_caller_id()+"STOPPING RECORDING BUMP")    
        if 'procMessage' in globals():
            rospy.loginfo(rospy.get_caller_id()+"Killing Rosbag")
            terminate_ros_node("/record")
    #print count, recordedBump
    

def sonarCallback(data):
    global count
    #rospy.loginfo(rospy.get_caller_id()+"Sonar Value")
    #print ("Sonar Value : %f " % (data.ranges))
    #print "Sonar Data Ranges", data.ranges
    for x in range(len(data.ranges)):
        if (data.ranges[x] < 0.2):
            print "Sonar Data Range", data.ranges
            sonar_mongo_record(data)
    #sonar_record(data)

def sonar_mongo_record(data):
    global sonarCollection

    sonar_id = mongoLABhelper.addSonarData(sonarCollection, data.ranges[0], data.ranges[1], data.ranges[2], data.ranges[3], data.ranges[4],
                                         data.ranges[5], data.ranges[6], data.ranges[7], data.ranges[8],
                                         data.ranges[9], data.ranges[10], data.ranges[11], data.ranges[12],
                                         data.ranges[13], data.ranges[14], data.ranges[15], data.ranges[16],
                                         data.ranges[17], data.ranges[18], data.ranges[19], data.ranges[20],
                                         data.ranges[21], data.ranges[22], data.ranges[23])
    #print collection.find_one(sonar_id)

def sonar_record(data):
    global t
    global recordedSonar
    #global procMessage
    #print "Some Sonar Data below 0.2"
    for x in range(len(data.ranges)):
        if (data.ranges[x] < 0.2 and recordedSonar == False):
            #print ("BAZINGA BAZINGA BAZINGA") 
            rospy.loginfo(rospy.get_caller_id()+"Start Recording! SONAR")
            global procMessage
            t = time.time() 
            recordedSonar = True
            procMessage = subprocess.Popen(["rosbag", "record", "-a","-o", "SonarBag"], preexec_fn=os.setsid)
            #time.sleep(10)
  
    if((time.time() - t) >= 10 and recordedSonar == True):
        t = 0
        recordedSonar = False 
        rospy.loginfo(rospy.get_caller_id()+"STOPPING RECORDING SONAR")    
        if 'procMessage' in globals():
            rospy.loginfo(rospy.get_caller_id()+"Killing Rosbag")
            terminate_ros_node("/record")
    #print recordedSonar
        

def terminate_ros_node(s):
    list_cmd = subprocess.Popen("rosnode list", shell=True, stdout=subprocess.PIPE)
    list_output = list_cmd.stdout.read()
    retcode = list_cmd.wait()
    assert retcode == 0, "List command returned %d" % retcode
    for str in list_output.split("\n"):
        if (str.startswith(s)):
            os.system("rosnode kill " + str)


def listener():
    # in ROS, nodes are unique named. If two nodes with the same
    # node are launched, the previous one is kicked off. The 
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'talker' node so that multiple talkers can
    # run simultaenously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/motor_state", MotorState, bump_callback)
    rospy.Subscriber("/sonar", SonarArray, sonarCallback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
        
if __name__ == '__main__':
    global count
    global recordedBump
    recordedBump = False
    global recordedSonar
    recordedSonar = False
    count = 0
    t = 0
    global sonarCollection
    global bumpCollection
    sonarCollection = mongoLABhelper.startSonarDatabaseURI("SonarCollection", "uri")
    bumpCollection = mongoLABhelper.startBumpDatabaseURI("bumpCollection", "uri")




    listener()

