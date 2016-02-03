import socket
import pickle
import os
import glob




def find_existing_files(): # makes a list of the existing saved files
    os.chdir(os.getcwd()+'\cloud')
    list = glob.glob('*.*')
    return list

def get_client_list(): # gets the files thet are supposed to be sinc'ed from the client
    client_list = client.recv(2048) #recv 1
    client_list2 = pickle.loads(client_list)
    return client_list2

def compare_lists(list,client_list): # compares the list of existing files and the list of files sent from the client to create 2 new lists: files that need to be sent from the client and files that need to be remoced from the server
    remove = []
    need = []

    for c in client_list:
        b = True
        for l in list:
            if c == l:
                b = False
        if b:
            need.append(c)

    for l in list:
        b = True
        for c in client_list:
            if l == c:
                b = False
        if b:
            remove.append(l)
    print need
    print remove
    return [need,remove]

def delete(remove): # deletes all the files that are no longer needed from memory
    for r in remove:
        os.remove(r)

def request_files(need): # requests the missing files from the client
    client.send(pickle.dumps(need)) #send 1

def get_files(need): # gets the files from the client
    for n in need:

        file = open(n,"wb")

        file_data = client.recv(1024)
        while (file_data[-5:] != "False"):
            file.write(file_data)
            file_data = client.recv(1024) #recv 2
        file_data = file_data[:-5]
        file.write(file_data)
        file.close()


sock = socket.socket()
sock.bind(('127.0.0.1', 12345))
sock.listen(1)
(client, address) = sock.accept()
list = find_existing_files()
client_list = get_client_list()
compared = compare_lists(list, client_list)
need = compared[0]
remove = compared[1]
delete(remove)
request_files(need)
get_files(need)