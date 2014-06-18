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
import fnmatch
import bag_Database

DB_NAME = "bagDB.db"


if __name__ == '__main__':

    bagname = ''
    topic = ''

    ###############################
    # o == option
    # a == argument passed to the o
    ###############################
    # Cache an error with try..except 
    # Note: options is the string of option letters that the script wants to recognize, with 
    # options that require an argument followed by a colon (':') i.e. -i fileName
    #
    try:
        myopts, args = getopt.getopt(sys.argv[1:],"b:t:")
    except getopt.GetoptError as e:
        print (str(e))
        print("Usage: %s -b bagname -t topic " % sys.argv[0])
        sys.exit(2)
     
    for o, a in myopts:
        if o == '-b':
            bagname=a
        if o == '-t':
            topic=a
            print topic
    bag_Database.openDatabase(DB_NAME)
    # Display input and output file name passed as the args
    print ("Bagname : %s " % (bagname))
    
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*.bag'):
            print ("Bag files: %s" % (file))
            if not bag_Database.bagExists(file):               
                userID = bag_Database.addNewBag(file)
                print userID
                bag_Database.setFileName(userID, file)
                print bag_Database.getFileName(userID)
                info_dict = yaml.load(subprocess.Popen(['rosbag', 'info', '--yaml', file], stdout=subprocess.PIPE).communicate()[0])
                topic_dict = info_dict['topics']
                length = len(topic_dict)
                y = ''
                for x in range(0, length):
                    print topic_dict[x]['topic'
                    y += topic_dict[x]['topic']
                bag_Database.setTopics(userID, y)
                print bag_Database.getTopics(userID)
            else:
                print ("Bag already Exists %s " % (file))

    print "KEYS TEST"
    for key in bag_Database.getUserIds():
        if topic in bag_Database.getTopics(key):
            print "DUDE"
            print bag_Database.getFileName(key)
            print bag_Database.getTopics(key)


    print bag_Database.getNumberOfBags()    
    bag_Database.CloseDatabase(DB_NAME)


