import socket
from Tkinter import *
from Tkconstants import *
import socket,thread
import os
import time
import sys
from threading import Lock
import random
import subprocess
import getopt
from time import time
import shutil
import string
host='169.254.168.249'
port=50007
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))


#print(repr(data))

def pickjob(*args):
	print("Pickin up a job")
	print("%s"%args[0])
	file1 = args[0]
        f=open(file1,"r")
        lines = f.readlines()
        f.close()
        for i in lines:
                sleeptime=1
                execute=i.split()
                print "execution length" +str(len(execute))
                if len(execute)>0:
                        if execute[0] == "pause":
                                if (len(execute)>2):
                                        sleeptime=execute[1]
                                        rest.append("pause" +str(sleeptime)+"\n")
                                        time.sleep(sleeptime)
                        print "nothing to do => sleeping for "+str(sleeptime)+".000 milliseconds\n"
                        if execute[0] == "quit":
                                os.remove(file1)
                        else:
                                f=open(file1,"r")
                                t=f.read()
                                f.close()
                                f=open(file1+".started","a")
                                f.write(i)
                                f.close()
                                os.system(i)
                                f=open(file1+".fnshd","a")
                                f.write(i)
                                f.close()

	return
def abc():
        
        print ("h264 Here we GO !!!!!! :D ")
        k=s.recv(1024)
	print k
        fp=open("client/global.jobs","w")
        print "hi"
        fp.write("client\\"+ k)
        fp.close()
        r=k.split("\\")
        print r

        print r[-1]
        firstsplit=r[-1].split('-')
        secondsplit=firstsplit[-1].split('.')
        fil=r[-1].split()
        s.send(fil[0])
        k=s.recv(200)
        print k
        fp=open("client/"+temp+"/"+fil[0],"w")
        fp.write(k)
        fp.close()
        #t=raw_input("Enter your choice: ")
        pickjob("client/global.jobs")
        passx264_c(temp,secondsplit[0])
        #t=raw_input("Enter your choice: ")
       # fp=open("C:/Python26/client/1.avi","wb")
        #k=s.recv(1024)   
        #while k:
         #       fp.write(k)
          #      k=s.recv(4096)
           #     print "chunk1 recived"
        yellow="stageC-"+str(secondsplit[0])+".264"
        s.send(yellow)
        fp=open("client/"+temp+"/"+"stageC-"+str(secondsplit[0])+".264","rb")
        k=fp.readlines()
        fp.close()
        for i in k:
                print (i)                
                s.send(i)
    

        print "done "
        s.close()
        os.system("start python client\clientelfinal11.py")       
        #break
        return

def passx264_c(*args):
                
        print ("passx264 C Stage ")
        temp=args[0]
        it=args[1]      
        global params,maxpar,avgchunk,chunks,chunksize,stageAjobs,default_options,totalbytes,frames,fps,totalbitrate,jobqueue
        global pathtox246,pass1opts,width,height,source,start_time,tfp,assign,targetrate
        fp=open("client/"+temp+"/projecthash.txt")
        lines=fp.read()
        k=lines.split()
        print k
        fp.close()
        width=k[1]
        height=k[3]
        source=k[5]
        temp=k[7]
        frames=k[9]
        totalbitrate=k[11]
        minchunksize=k[13]
        start_time=float(k[15])
        print start_time
        totalbytes=k[17]
        output=k[19]
        chunks=int(k[21])
        maxpar=k[23]
        pass2opts=k[25]+" "+str(k[26])+" "+k[27]+str(k[28])
        pass1opts=k[30]+" "+str(k[31])+" "+k[32]+str(k[33])
        pathtox246=k[35]
        print pathtox246
        jobqueue=k[37]
        fps=float(k[39])
        #starttime=time()
        #get_frames_fps_resolution()
       	#print "collecting Stage A results %s chunks in total)\n"%str(chunks)
       	fp=open("client/"+temp+"/stageA.jobs","r")
       	stageAjobs=fp.readlines()
       	fp.close()
       	#for i in range(0,chunks,1):
               # chunknum=i+1
                #print chunknum
                #print "chunks"+ str(chunks)
                #a=raw_input()
                #progress=int(100*chunknum/int(chunks))
                #passed=time()-start_time
                #framessofar=int(stageAjobs[2*i+1])+1
                #print framessofar
                #print ("stage A progress:"+ str(int(chunknum)/int(chunks))+ "chunks done" +str(progress)+"%in"+str(passed) +"seconds." +str(framessofar)+" frames so far.\n")
        r="client/"+temp+"/stageA-"+str(it)+".264"
                #print r
        tfp=0
        chunksizer=os.path.getsize(r)
        print chunksizer
#        assign.append(chunksizer/(1024*1024))
        tfp=tfp+chunksizer
        print "Stage A completed\n"
        
        start_timepass2=time()
        stageCjobs=stageAjobs
       	#for i in range(0,chunks,1):
               
        chunktarget=int(chunksizer)*int(totalbytes)/int(tfp)
        print "red" +str(chunktarget)
               # a=raw_input()
        chunkframes=int(stageCjobs[1+2*int(it)])-int(stageCjobs[2*int(it)])+1
        print "chunkframe" +str(chunkframes)
              #  a=raw_input()
        chunkrate=round((float(fps)*chunktarget)*8/(chunkframes*1024*1024) )
        print chunkrate
       # print "heyyaaaa"+str(targetrate)
#        a=raw_input()
        fp=open("client/global.jobs","w")
       	#for i in range(0,chunks,1):
              #os.remove(temp+"/stageA-result"+str(i)+".ready")
              #os.remove(temp+"/stageC-result"+str(i)+".ready")
        filename="client/"+temp+"/stageC-"+str(it)+".bat"
        l=open("client/"+temp+"/stageC-"+str(it)+".bat","w")
        seek=int(stageAjobs[int(it)*2])
        frames1=int(stageAjobs[int(it)*2+1])-int(stageAjobs[int(it)*2])+1
        rate=chunkrate
        print pathtox246
#        a=raw_input()
              #              command="cd " +str(temp) +"\nstart /belownormal /B /wait "+str(pathtox246)+" --progress --seek "+ str(seek) +"--frames " +str(frame1)+" --crf 24 " +pass1opts+" -p 1 --stats stageA-"+str(i)+".stats -o stageA-"+str(i)+".264 source.avs \necho.> stageA-result"+str(i)+".ready\n";
        command1="cd client/" +str(temp);
        command2 = "\nstart /belownormal /B /wait ..//x264.exe --progress --seek "+str(seek)+" --frames " +str(frames1);
        command3 = " -B 11 -p 3 --stats stageA-"+str(it)+".stats -o stageC-"+str(it)+".264 -b2 -m6 source.avs \necho.> stageA-result"+str(it)+".ready\necho.> stageC-result"+str(it)+".ready\n";
                

#              abc="cd "+str(temp)+"\nstart /belownormal /B /wait "+str(pathtox246)+" --progress --seek "+str(seek)+" --frames "+str(frames1)+" -B "+ str(rate)+" -p 3 --stats stageA-"+str(i)+".stats -o stageC-"+str(i)+".264 "+str(pass1opts)+" source.avs\necho.> stageA-result"+str(i)+".ready\necho.> stageC-result"+str(i)+".ready\n"
             
        l.write(command1)
        l.write(command2)
        l.write(command3)
              
        l.close()
        rat="client\\"+str(temp)+"\\stageC-"+str(it)+".bat\n"
        print rat
#        a=raw_input()
        fp.write(rat)
        fp.close()
        fp=open("client/"+temp+"/stageC.jobs","w")
        for i in stageCjobs:
                fp.write("client/"+str(it)+"\n")
        fp.close()
        fp=open("client/"+temp+"/projecthash.txt","w")
        fp.write("\nwidth\n"+str(width)+"\nheight\n"+str(height)+"\nsource\n"+str(source)+"\ntmpdir\n"+str(temp)+"\nframes\n"+str(frames)+"\ntotalbitrate\n -1"+"\nminchunksize\n"+
str(minchunksize)+"\nstart_time\n"+str(start_time)+"\ntotalbytes\n"+str(totalbytes)+"\noutput\n"+str(output)+"\nchunks\n"+str(chunks)+"\nmaxpar\n"+str(maxpar)+"\npass2opts\n"+str(pass1opts)+"\npass1opts\n"+str(pass1opts)+"\npathtox246\n"+str(pathtox246)+"\njobqueue\n"+str(jobqueue)+"\nfps\n"+str(fps)+"\ntimesecondpass\n"+str(start_timepass2))
        fp.close()

        print "exiting stage c...... "
        pickjob("client/global.jobs")
        return
    
      

                
temp=s.recv(1024)
if not os.path.exists("client/"+temp):
        s.send(str(1))
        print temp
        os.makedirs("client/"+temp)
        k=s.recv(72)
        print k
        fp=open("client/"+temp+"/parameters.txt","w")
        fp.write(k)
        fp.close()
        k=s.recv(282)
        print k
        fp=open("client/"+temp+"/projecthash.txt","w")
        fp.write(k)
        fp.close()
        k=s.recv(100)
        print k
        fp=open("client/"+temp+"/source.avs","w")
        fp.write(k)
        fp.close()
        k=s.recv(160)
        print k
        fp=open("client/"+temp+"/stageA.jobs","w")
        fp.write(k)
        fp.close()
else:
        s.send(str(0))
abc()

