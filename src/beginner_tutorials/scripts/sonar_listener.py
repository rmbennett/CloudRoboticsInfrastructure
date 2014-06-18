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
import mongohelper
from pymongo import MongoClient
#from p2os_driver.msg import MotorState
#from kinect import Kinect
#import audio_listener

def sonarCallback(data):
    global count
    #rospy.loginfo(rospy.get_caller_id()+"Sonar Value")
    #print ("Sonar Value : %f " % (data.ranges))
    #print "Sonar Data Ranges", data.ranges
    #print len(data.ranges)
    for x in range(len(data.ranges)):
        if (data.ranges[x] < 0.2):
            print "Sonar Data Range", data.ranges
            #sonar_bag_record(data)
            sonar_mongo_record(data)

    #bump_record(data
    #audio_listener.setup()


def sonar_bag_record(data):
    global count
    global t
    global recorded

    if(recorded == False):     
        print ("BAZINGA BAZINGA BAZINGA")
        #count= count + 1 
        rospy.loginfo(rospy.get_caller_id()+"Start Recording!")
        global procMessage
        t = time.time() 
        recorded = True
        procMessage = subprocess.Popen(["rosbag", "record", "-a","-O", startValue], preexec_fn=os.setsid)
        #time.sleep(10)
  
    elif((time.time() - t) >= 10 and recorded == True):
        t = 0
        recorded = False 
        rospy.loginfo(rospy.get_caller_id()+"STOPPING RECORDING")    
        if 'procMessage' in globals():
            rospy.loginfo(rospy.get_caller_id()+"Killing Rosbag")
            #terminate_ros_node("/record")
    print recorded

def sonar_mongo_record(data):
    global collection
    sonar_id = mongohelper.addSonarData(collection, data.ranges[0], data.ranges[1], data.ranges[2], data.ranges[3], data.ranges[4],
                                         data.ranges[5], data.ranges[6], data.ranges[7], data.ranges[8],
                                         data.ranges[9], data.ranges[10], data.ranges[11], data.ranges[12],
                                         data.ranges[13], data.ranges[14], data.ranges[15], data.ranges[16],
                                         data.ranges[17], data.ranges[18], data.ranges[19], data.ranges[20],
                                         data.ranges[21], data.ranges[22], data.ranges[23])
    print collection.find_one(sonar_id)

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

    rospy.Subscriber(topic, SonarArray, sonarCallback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
        
if __name__ == '__main__':
    count = 0
    topic=''
    recorded = False
    global collection
    collection = mongohelper.startDatabase("test_database", "sonarTest")

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
    topic = "/sonar"
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