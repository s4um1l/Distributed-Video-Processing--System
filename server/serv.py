from Tkinter import *
import socket,thread
from Tkconstants import *
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
#import FCNTL
params=''
preferredchunksize=100
minchunksize=80
magicfactor=1.00
chunks=0
stageAjobs=[]
source=''
start_time=0
targetrate=[]
queen=[]
tfp=0
assign=[]                                                                             
def version():
	print ("Hello")
	return

def resume():
	print("Resume on")
	return
def shutdown():
	print("Shutting d system down ;)")
	os.rename("global.jobs","global.jobs.save")
	os.rename("control.jobs","control.jobs.save")
	INFO=open("global.jobs","w")
	INFO.write("quit\n")
	INFO.close()
	INFO=open("control.jobs","w")
	INFO.write("quit\n")
	INFO.close()
	#lock.unlock()
	#lock1.unlock()
	time.sleep(2)
	#lock.unlock()
	#lock1.unlock()
	return
def spawn(*args):
	print ("dun knoe wh ")
	print (args[1])
#	for i in range(0,args[0],1):
        a="python try1.py pickjob " + args[1]
        os.system(a)
        return
def spawnmax():
	print ("hehe")
	print (sys.argv[2])
	a="python try1.py pickjob " + sys.argv[2]
	os.system(a)
	return
def pickjob():
	print("Pickin up a job")
	print("%s"%sys.argv[2])
	file1 = sys.argv[2]
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



        
     
	return
def print_1passtime(*argvs):
        global pass1fps
        # print 1st pass time
	passed=time()-argvs[1]
	pass1fps=int(100*int(argvs[0])/passed)/100
	print "1st pass fps = %f\n" % pass1fps
        return
def h264():
        global temp
	print ("h264 Here we GO !!!!!! :D ")
	temp=str(int(random.randint(1,1000000)))
	os.makedirs(temp)
	fp=open("resume.bat","a")
	fp.write("python try1.py resume "+temp + "\n")
 	fp.close()
	fp= open(temp+"/parameters.txt","w")
        l=len(sys.argv)
	for i in range(1,l,1):
		fp.write(sys.argv[i]+"\n")
	fp.close()
	fp=open("control.jobs","w")
	#FCNTL.flock(fp.fileno(), FCNTL.LOCK_EX)
	fp.write("python try1.py h264a "+temp + "\n")
	fp.write("python try1.py pass_x264_c "+temp + "\n")
	fp.write("python try1.py h264d "+temp + "\n")
 	fp.close()
	print "encode job %s set up\n" % temp;
	print temp
	pass_xva(temp)
	return



def pass_xva(*args):
        print args[0]
        temp=args[0]
        global params,maxpar,avgchunk,chunks,chunksize,stageAjobs,default_options,totalbytes,frames,fps,totalbitrate,jobqueue
        global pathtox246,pass1opts,width,height,source,start_time
        default_options="-b 2 -m 3"
       # fp=open(str(temp)+"/parameters.txt","r")
       # params=fp.read()
       # fp.close()
        #print params
        get_params()
        starttime=time()
        get_frames_fps_resolution()
        shutil.copy2(source, temp+"/source.avs")

        compute_chunks()
        avgchunk=round(chunksize)
        print "using %s threads to encode %s chunks of about %s frames\n" % (maxpar,chunks,avgchunk)
        if (int(maxpar)>int(chunks)):
                print "warning: less chunks than available threads!\n"
        compute_aranges()
        if totalbytes==0:
                totalbytes=round(int(totalbytes)*int(totalbitrate)*128*int(frames)/int(fps))
                mbytes=int(100*totalbytes/1024/1024)/100
                print "target size is %f bytes %f MB)\n" %(totalbytes,mbytes)
        print jobqueue
        fp=open(jobqueue,"w")
        for i in range(0,chunks,1):
                seek=stageAjobs[i*2]
                frame1=stageAjobs[i*2+1]-stageAjobs[i*2]+1
                print frame1,i
                filename=temp+"/stageA-"+str(i)+".bat"
                f=open(filename,"w")
                command="cd " +str(temp) +"\nstart /belownormal /B /wait "+str(pathtox246)+" --progress --seek "+ str(seek) +" --frames " +str(frame1)+" --crf 24 " +pass1opts+" -p 1 --stats stageA-"+str(i)+".stats -o stageA-"+str(i)+".264 source.avs \necho.> stageA-result"+str(i)+".ready\n";
                command.replace("--seek 0",'');
                f.write(command)
                f.close()
                fp.write(str(temp)+"\\stageA-"+str(i)+".bat\n")
        fp.write("pause\n ")
        fp.close()
        fp=open(temp+"/stageA.jobs","w")
        for i in stageAjobs:
                fp.write(str(i)+"\n")
        print "Done till writing A jobs"        
        fp.close()
        fp=open(temp+"/projecthash.txt","w")
        fp.write("width\n"+str(width)+"\nheight\n"+str(height)+"\nsource\n"+str(source)+"\ntmpdir\n"+str(temp)+"\nframes\n"+str(frames)+"\ntotalbitrate\n -1"+"\nminchunksize\n"+
str(minchunksize)+"\nstart_time\n"+str(start_time)+"\ntotalbytes\n"+str(totalbytes)+"\noutput\n"+str(output)+"\nchunks\n"+str(chunks)+"\nmaxpar\n"+str(maxpar)+"\npass2opts\n"+str(pass1opts)+"\npass1opts\n"+str(pass1opts)+"\npathtox246\n"+str(pathtox246)+"\njobqueue\n"+str(jobqueue)+"\nfps\n"+str(fps))
        fp.close()
       
        print("Yeah !!!! thru from stage a !!!!!")
        
        return
def h264d():
	print ("x264 D Stage ")
	temp=sys.argv[2]
        global params,maxpar,avgchunk,chunks,chunksize,stageAjobs,default_options,totalbytes,frames,fps,totalbitrate,jobqueue
        global pathtox246,pass1opts,width,height,source,start_time
        #get_params()
        #starttime=time()
        #get_frames_fps_resolution()
        fp=open(temp+"/projecthash.txt")
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
        totalbytes=k[17]
        output=k[19]
        chunks=int(k[21])
        maxpar=k[23]
        pass2opts=k[25]+" "+str(k[26])+" "+k[27]+str(k[28])
        pass1opts=k[30]+" "+str(k[31])+" "+k[32]+str(k[33])
        pathtox246=k[35]
        jobqueue=k[37]
        start_time2=k[39]
        fp.close()
       	fp=open(temp+"/stageC.jobs","r")
       	r=fp.read()
       	fp.close()
        stageCjobs=r.split()
        print stageCjobs
       	print "collecting Stage C results %s chunks in total)\n"%str(chunks);
       	for i in range(0,chunks,1):
                chunknum=i+1
                copycommand="type "+str(temp)+"\stageC-"+str(i)+".264 >> "+str(temp)+"\\abc"
                print copycommand
                os.system(copycommand)
                os.remove(temp+"/stageC-"+str(i)+".264")                
                progress=int(100*chunknum/int(chunks))
                passed=time()-start_time
                framessofar=int(stageCjobs[2*i+1])+1
                print framessofar
                print ("stage C progress:"+ str(chunknum/int(chunks))+ "chunks done" +str(progress)+"%in"+str(passed) +"seconds." +str(framessofar)+" frames so far.\n")
        print "Stage C completed\n"
        print_totaltime()
        muxavc()
        compare_outputsize()
        print "another job well done\n";
	return
def muxavc():
        global fps,output
        temp=sys.argv[2]
        fp=open(temp+"/projecthash.txt")
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
        totalbytes=k[17]
        output=k[19]
        chunks=int(k[21])
        maxpar=k[23]
        pass2opts=k[25]+" "+str(k[26])+" "+k[27]+str(k[28])
        pass1opts=k[30]+" "+str(k[31])+" "+k[32]+str(k[33])
        pathtox246=k[35]
        jobqueue=k[37]
        fps=k[39]
      
	print output
	print "muxing to .mp4\n"
	os.system("mp4box -cat "+str(temp)+"/abc -fps "+str(fps)+" -new "+output+" 1>NUL 2>NUL")
	print "chunks merged\n";
	return

def print_totaltime():
        global start_time,overallfps,frames
	passed=time()-start_time
	print "total time for encoding: %f seconds\n"%passed
	overallfps=int(100*int(frames)/passed)/100;
	print "overall fps =%d \n"%overallfps;
        return
def compare_outputsize():
        global output,totalbytes
	encodedbytes=os.path.getsize(output);
	print encodedbytes
	if totalbytes==-1:
                totalbytes=encodedbytes
	error=round(10000*abs(totalbytes-encodedbytes)/totalbytes)/100;
	sign="+"
	if totalbytes > encodedbytes:
                	sign="-" 
	print "target:\t"+str(totalbytes)+" bytes\nencode:\t"+str(encodedbytes)+" bytes\nerror:\t"+str(sign)+str(error)+"%\n"

def passx264_c():
                
        print ("passx264 C Stage ")
        temp=sys.argv[2]
      
        global params,maxpar,avgchunk,chunks,chunksize,stageAjobs,default_options,totalbytes,frames,fps,totalbitrate,jobqueue
        global pathtox246,pass1opts,width,height,source,start_time,tfp,assign,targetrate
        fp=open(temp+"/projecthash.txt")
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
        totalbytes=k[17]
        output=k[19]
        chunks=int(k[21])
        maxpar=k[23]
        pass2opts=k[25]+" "+str(k[26])+" "+k[27]+str(k[28])
        pass1opts=k[30]+" "+str(k[31])+" "+k[32]+str(k[33])
        pathtox246=k[35]
        jobqueue=k[37]
        fps=float(k[39])
        #starttime=time()
        #get_frames_fps_resolution()
       	print "collecting Stage A results %s chunks in total)\n"%str(chunks)
       	fp=open(temp+"/stageA.jobs","r")
       	stageAjobs=fp.readlines()
       	fp.close()
       	for i in range(0,chunks,1):
                chunknum=i+1
                print chunknum
                progress=int(100*chunknum/int(chunks))
                passed=time()-start_time
                framessofar=int(stageAjobs[2*i+1])+1
                print framessofar
                print ("stage A progress:"+ str(int(chunknum)/int(chunks))+ "chunks done" +str(progress)+"%in"+str(passed) +"seconds." +str(framessofar)+" frames so far.\n")
                r=temp+"/stageA-"+str(i)+".264"
                print r
                tfp=0
                chunksizer=os.path.getsize(r)
                print chunksizer
                assign.append(chunksizer)
                tfp=tfp+chunksizer
        print "Stage A completed\n"
        print_1passtime(frames,start_time)
        start_timepass2=time()
        stageCjobs=stageAjobs
       	for i in range(0,chunks,1):
               
                chunktarget=int(assign[i])*int(totalbytes)/int(tfp)
                print "red" +str(chunktarget)
               # a=raw_input()
                chunkframes=int(stageCjobs[1+2*i])-int(stageCjobs[2*i])+1
                print "chunkframe" +str(chunkframes)
              #  a=raw_input()
                chunkrate=round((float(fps)*chunktarget)*8/(chunkframes*1024) )
                print chunkrate
                targetrate.append(chunkrate)
        print "heyyaaaa"+str(targetrate)
        
        fp=open(jobqueue,"w")
       	for i in range(0,chunks,1):
              #os.remove(temp+"/stageA-result"+str(i)+".ready")
              #os.remove(temp+"/stageC-result"+str(i)+".ready")
              filename=temp+"/stageC-"+str(i)+".bat"
              l=open(temp+"/stageC-"+str(i)+".bat","w")
              seek=int(stageAjobs[i*2])
              frames1=int(stageAjobs[i*2+1])-int(stageAjobs[i*2])+1
              rate=targetrate[i]
#              command="cd " +str(temp) +"\nstart /belownormal /B /wait "+str(pathtox246)+" --progress --seek "+ str(seek) +"--frames " +str(frame1)+" --crf 24 " +pass1opts+" -p 1 --stats stageA-"+str(i)+".stats -o stageA-"+str(i)+".264 source.avs \necho.> stageA-result"+str(i)+".ready\n";
              command1="cd " +str(temp);
              command2 = "\nstart /belownormal /B /wait "+str(pathtox246)+" --progress --seek "+str(seek)+" --frames " +str(frames1);
              command3 = " -B " +str(int(rate))+" -p 3 --stats stageA-"+str(i)+".stats -o stageC-"+str(i)+".264 "+str(pass1opts)+" source.avs \necho.> stageA-result"+str(i)+".ready\necho.> stageC-result"+str(i)+".ready\n";
                

#              abc="cd "+str(temp)+"\nstart /belownormal /B /wait "+str(pathtox246)+" --progress --seek "+str(seek)+" --frames "+str(frames1)+" -B "+ str(rate)+" -p 3 --stats stageA-"+str(i)+".stats -o stageC-"+str(i)+".264 "+str(pass1opts)+" source.avs\necho.> stageA-result"+str(i)+".ready\necho.> stageC-result"+str(i)+".ready\n"
             
              l.write(command1)
              l.write(command2)
              l.write(command3)
              
              l.close()
              fp.write(str(temp)+"\\stageC-"+str(i)+".bat\n")
        fp.close()
        fp=open(temp+"/stageC.jobs","w")
        for i in stageCjobs:
                fp.write(str(i)+"\n")
        fp.close()
        fp=open(temp+"/projecthash.txt","w")
        fp.write("width\n"+str(width)+"\nheight\n"+str(height)+"\nsource\n"+str(source)+"\ntmpdir\n"+str(temp)+"\nframes\n"+str(frames)+"\ntotalbitrate\n -1"+"\nminchunksize\n"+
str(minchunksize)+"\nstart_time\n"+str(start_time)+"\ntotalbytes\n"+str(totalbytes)+"\noutput\n"+str(output)+"\nchunks\n"+str(chunks)+"\nmaxpar\n"+str(maxpar)+"\npass2opts\n"+str(pass1opts)+"\npass1opts\n"+str(pass1opts)+"\npathtox246\n"+str(pathtox246)+"\njobqueue\n"+str(jobqueue)+"\nfps\n"+str(fps)+"\ntimesecondpass\n"+str(start_timepass2))
        fp.close()

        print "exiting stage c...... "
        spawn(2,"global.jobs")
        return

      

                

def compute_aranges():
        global stageAjobs,frames,chunks,chunksize
        currentframe=0
        stageAjobs.append(currentframe)
        print "HI"
        
        for i in range(0,chunks-1,1):
                currentframe+=chunksize
                stageAjobs.append(currentframe)
                stageAjobs.append(currentframe+1)
               
        stageAjobs.append(int(frames)-1)
        print stageAjobs
        return
def compute_chunks():
        global chunks,preferredchunksize,frames,maxpar,chunksize
        if chunks==0:
                chunks=int(frames)/int(preferredchunksize)
        if int(chunks) < int(maxpar):
                chunks=maxpar
        chunksize=int(frames)/int(chunks)
        if int(chunksize)<int(minchunksize):
                chunks=int(frames)/int(minchunksize)
                chunksize=minchunksize
                
        print chunks,chunksize
        return
def get_params():
        global params,jbq,source,maxpar,output,totalbytes,pass1opts,pass2opts,pathtox246
        jbq=""
        totalbytes=0
        pass1opts=''
        pass2opts=''
        maxpar=0
        output=''
        r=params.split()
        opt,args=getopt.getopt(r,'b:s:j:f:c:o:m:p:a:q:t:r:')
        x=len(opt)
        print opt
        for i in range(0,x,1):
                if opt[i][0]=="-j":
                        if opt[i][0]=="-j":
                                print"Hi:"
                                jbq=opt[i][1]
                        else: 
                                jbq=''
                if opt[i][0]=="-a":        
                        if opt[i][0]=="-a":
                                source=opt[i][1]
                        else: 
                                source="default.avs"
                if opt[i][0]=="-o":
                        if opt[i][0]=="-o":
                                output=opt[i][1]
                        else: 
                                output="output.mp4"
                if opt[i][0]=="-m":
                        if opt[i][0]=="-m":
                                print opt[i][1]
                                maxpar=opt[i][1]
                        else:
                                maxpar=0
                if opt[i][0]=="-s":
                        if opt[i][0]=="-s":
                                print opt[i][1]
                                totalbytes=opt[i][1]
                        else:
                                totalbytes=0
        pass1opts=default_options
        pass2opts=default_options
        pathtox246="..//x264.exe"
        print jbq,source,maxpar,output,totalbytes,pass1opts,pass2opts
        print "The Input Characterstics :D after a long struglle conquered "

        return
def encode_percent():
	print ("encoded percentage")
	return
def find_resolution():
	print ("resolution ")
	return
def get_frames_fps_resolution():
        global frames,width,height,fps
        print ("fps resolution")
        os.system("avs2avi.exe C:\Python26\default.avs -o l >t.txt")
        fp=open("t.txt","r")
        lineList=fp.readlines()
        fp.close()
        for line in lineList:
               if line.find("Frames:")>0:
                       #print line
                       b=line.split()
                       print b[-1]
                       frames=b[-1]
                       print frames
               if line.find("Resolution:")>0:
                       c=line.split('x')
                       
                       print c[-1]
                       height=c[-1]
                       d= c[-2].split()
                       width=d[-1]
                       print width
               if line.find("Frame rate:")>0:
                       c=line.split()
                       print c[-2]
                       fps=c[-2]
                                       
                
        return


host=''
port=50007
s=socket.socket()
s.bind((host,port))
s.listen(5)
msg="1.Copy a file\n2.Append data in the file\n3.Trace the file \n4.exit"
def handleclient(conn):
    while True:
	conn.send(msg)
        data=conn.recv(1204)
        if not data:
            break
	if data=="1":
		conn.send("enter the file name with path: ")
		data=conn.recv(1204)
		file1=open(data,'r')
		file2=open(os.path.basename(data),'w')
		for line in file1.readlines():
			file2.writelines(line)
		file1.close()
		file2.close()
		conn.send("\n\nFile Copied...\n\n")
	elif data=="2":
		conn.send("Enter the data to be appended: ")
		data=conn.recv(1204)
		file2=open('server.txt','a')
		file2.writelines(data)
		file2.close()
		conn.send("\n\nData appended\n\n")
	elif data=="3":
		conn.send("Enter cursor position from where you want to trace the file: ")
		data=conn.recv(1204)
		d=int(data)
		file2=open('server.txt','r')
		z=1
		for z in range (0,d,1):
			ch=file2.read(1)
		file_stats = os.stat('server.txt')
		p=file_stats [stat.ST_SIZE]
		for z in range (d,p,1):
			ch+=file2.read(1)
		conn.send(ch)
	else :
		conn.close()
	
while True:
    conn,addr=s.accept()
    print "Server Initiliazation....................."
    h264()
    
    print 'connected to ',addr
    thread.start_new_thread(handleclient,(conn,))








