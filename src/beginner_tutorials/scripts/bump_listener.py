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
from p2os_driver.msg import MotorState
import mongohelper
from pymongo import MongoClient
#from kinect import Kinect
#import audio_listener

def bump_callback(data):
    #bump_bag_record(data)
    bump_mongo_record(data)


def bump_mongo_record(data):
    global collection

    bump_id = mongohelper.addBumpData(collection, data.state)
    
    print collection.find_one(bump_id)

def bump_bag_record(data):
    global count
    global t
    global recorded
    print ("Motor State Value : %s " % (data))
    if(data.state == 0 and count == 0):     
        print ("BAZINGA BAZINGA BAZINGA")
        count= count + 1 
        rospy.loginfo(rospy.get_caller_id()+"Start Recording!")
        global procMessage
        t = time.time() 
        recorded = True
        procMessage = subprocess.Popen(["rosbag", "record", "-a","-O", startValue], preexec_fn=os.setsid)
        #time.sleep(10)
    
    elif(data.state == 0 and not count == 0 and not count == 10):
         global count
         count = count + 1

    elif(count == 10):
        global count
        count = 0
    
    elif((time.time() - t) >= 10 and recorded == True):
        t = 0
        recorded = False 
        rospy.loginfo(rospy.get_caller_id()+"STOPPING RECORDING")    
        if 'procMessage' in globals():
            rospy.loginfo(rospy.get_caller_id()+"Killing Rosbag")
            terminate_ros_node("/record")
    print count, recorded
    
        

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
    #rospy.init_node('kinect_listener', anonymous=True)

    rospy.Subscriber(topic, MotorState, bump_callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
        
if __name__ == '__main__':
    global count
    global recorded
    recorded = False
    count = 0
    topic=''
    t = 0
    global collection
    collection = mongohelper.startDatabase("test_database", "BumpTest")

    # startValue='' 
    # endValue=''


    ###############################
    # o == option
    # a == argument passed to the o
    ###############################
    # Cache an error with try..except 
    # Note: options is the string of option letters that the script wants to recognize, with 
    # options that require an argument followed by a colon (':') i.e. -i fileName
    #
    # try:
    #     myopts, args = getopt.getopt(sys.argv[1:],"t:s:e:")
    # except getopt.GetoptError as e:
    #     print (str(e))
    #     print("Usage: %s -t Topic -s Start Value -e End Value" % sys.argv[0])
    #     sys.exit(2)
     
    # for o, a in myopts:
    #     if o == '-t':
    #         topic=a
    #     elif o == '-s':
    #         startValue=a
    #     elif o == '-e':
            # endValue=a     
    topic = "/motor_state"
    # Display input and output file name passed as the args
    #print ("Topic : %s and StartValue: %s and End Value: %s " % (topic, startValue, endValue))
    #bagname  = "Topic: "+topic+ " Started on: " +startValue+" Stopped on: "+endValue
    #print(bagname)
    #test = rospy.get_param("~param") 
    #rospy.loginfo(test)
    #bag = rosbag.Bag('Specialtest.bag', 'w')
    #str = String()
    #str.data = 'foo'
    #bag.write('chatter', str)
    listener()
    #bag.close()
    #bag = rosbag.Bag('Subprocess_2014-04-28-16-39-15.bag')
    #for topic, msg, t in bag.read_messages(topics=['chatter', 'badger']):
    #    print msg
    #bag.close()

    #os.remove("/home/rmb209/rosgroovy/"+bagname)
