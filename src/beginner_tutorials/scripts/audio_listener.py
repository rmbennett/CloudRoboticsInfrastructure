#!/usr/bin/python
import rospy
import pyaudio
import subprocess
import os
import math
import struct
import wave
import time
import sys
from time import gmtime, strftime
from wit import Wit
from geometry_msgs.msg import Twist
import mongohelper
from pymongo import MongoClient
import smtplib
from threading import Thread

witInstance = Wit('WITIDHERE')
#Assuming Energy threshold upper than 30 dB
Threshold = 100

SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2
Max_Seconds = 3
TimeoutSignal=((RATE / chunk * Max_Seconds) + 2)
TimeoutSignal2=((RATE / chunk * Max_Seconds) + 100)
silence = True
Time=0


def GetStream(chunk):
    return stream.read(chunk)

def send_async_email(msg):

        fromaddr = ''
        toaddrs  = ''

        # Credentials (if needed)
        username = ''
        password = ''

        # The actual mail send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()


def rms(frame):
        count = len(frame)/swidth
        format = "%dh"%(count)
        shorts = struct.unpack( format, frame )

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n*n
        rms = math.pow(sum_squares/count,0.5);
        #print rms*1000
        return rms * 1000

def wit_mongo_record(data):
    global collection
    #print collection
    #print witOutput
    try:
        wit_id = mongohelper.addSpeechData(collection, data)
    except :
        print "Error"
    print wit_id
    print collection.find_one(wit_id)

def WriteSpeech(WriteData):
    global stream
    global p
    global pub
    global cmd
    
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    FileNameTmp = '/home/rmb209/wavefile'+strftime("%Y-%m-%d %H:%M:%S", gmtime())+'.wav'
    wavefile = FileNameTmp
    wf = wave.open(wavefile, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(WriteData)
    wf.close()

    witOutput = "Empty"
    sound = open(wavefile)    
    try:
        t = time.time()
        witOutput = witInstance.post_speech(sound)
        a = time.time() - t
        print a
        
        
    except:
        pass
    if witOutput != "Empty":
        wit_mongo_record(witOutput)
        print witOutput["outcome"]["intent"]

        os.rename(FileNameTmp, '/home/rmb209/RosSpeechFile_'+witOutput["msg_body"]+strftime("%Y-%m-%d %H:%M:%S", gmtime())+'.wav')

        msg = 'Subject: %s\n\n%s' % ("Audio has been heard", witOutput["msg_body"])

        thr = Thread(target = send_async_email, args =[msg])
        thr.start()




    else:
        os.remove(FileNameTmp)
    


   
    p = pyaudio.PyAudio()

    stream = p.open(format = FORMAT,
        channels = CHANNELS,
        rate = RATE,
        input = True,
        output = True,
        frames_per_buffer = chunk)



def KeepRecord(TimeoutSignal, LastBlock):

    all = []
    all.append(LastBlock)
    for i in range(0, TimeoutSignal):
        try:
            data = GetStream(chunk)
        except:
            continue

        all.append(data)
    #print "end record after timeout";
    data = ''.join(all)
    #print "write to File";
    WriteSpeech(data)
    silence = True
    Time=0
   

def terminate_ros_node(s):
    list_cmd = subprocess.Popen("rosnode list", shell=True, stdout=subprocess.PIPE)
    list_output = list_cmd.stdout.read()
    retcode = list_cmd.wait()
    assert retcode == 0, "List command returned %d" % retcode
    for str in list_output.split("\n"):
        if (str.startswith(s)):
            os.system("rosnode kill " + str)

def listen(silence,Time):
    #print "waiting for Speech"
    global p
    global stream
    while silence:
        
        try:
            input = GetStream(chunk)
        except:
            print "GetStream Failed"
            continue

        rms_value = rms(input)

        if (rms_value > Threshold):

            silence=False
            LastBlock=input
            print "I'm Recording...."
            KeepRecord(TimeoutSignal, LastBlock)

        Time = Time + 1
        if (Time > TimeoutSignal2):
            print "Time Out so Restart"
            Time = 0
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            p = pyaudio.PyAudio()
            stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                frames_per_buffer = chunk)


def setup():
    global p
    p = pyaudio.PyAudio()
    global stream
    stream = p.open(format = FORMAT,
        channels = CHANNELS,
        rate = RATE,
        input = True,
        output = True,
        frames_per_buffer = chunk)
    while(True):
        listen(silence,Time)


if __name__ == '__main__':
    global pub
    global collection
    collection = mongohelper.startDatabase("test_database", "AudioTest")

    
    while(True):
        setup()