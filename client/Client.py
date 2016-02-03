import socket
import pickle
import os
import glob


def identify():
    username = raw_input("username:")
    password = raw_input("password:")
    sock.send(username)
    sock.send(password)
    print(sock.recv(1024))

def location_finder(): # finds the location of the folder that is going to be sinc'ed
    file = open("Location.txt","r")
    location = file.read()
    file.close()
    os.chdir(location)

def send_file_list(): # sends the list of existing files to the cloud server
    list = glob.glob('*.*')
    list2 = pickle.dumps(list)
    sock.send(list2)   #send 1

def files_to_be_sent(): # receives a list of files from the cloud that needs to be sent
    files_list = sock.recv(2048) #recv 1
    print(files_list)
    files_list2 = pickle.loads(files_list)
    return files_list2

def send_files(files_list): # sends the requested files to the cloud
    for i in files_list:

        file = open (i, "rb")
        file_data = file.read(1024)
        while (file_data):
            sock.send(file_data) #send 2
            file_data = file.read(1024)
        sock.send("False")
        file.close()

sock = socket.socket()
sock.connect(('127.0.0.1', 12345))
location_finder()
send_file_list()
files_list = files_to_be_sent()
send_files(files_list)