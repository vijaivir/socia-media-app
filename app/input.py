import requests
import sys
import time

apiUrl = "http://localhost:5000"

def createCommand(line):
    c = line.split(',')
    cmd = c[0].split(" ")[1]
    print(cmd)

    if(cmd == 'ADD'):
        requests.post(apiUrl + '/add', json={'cmd':cmd, 'username':c[1], 'dob':c[2], 'email':c[3], 'password':c[4]})
    elif(cmd == 'CREATE_POST'):
        requests.post(apiUrl + '/create_post', json= {'cmd':cmd, 'username':c[1], 'post':c[2]})
    elif(cmd == 'EDIT_POST'):
        requests.post(apiUrl + '/edit_post', json={'cmd':cmd, 'username':c[1], 'post_id':c[2], 'post':c[3]})
    elif(cmd == 'DELETE_POST'):
        requests.post(apiUrl + '/delete_post', json={'cmd':cmd, 'username':c[1], 'post_id':c[2]})
    elif(cmd == 'COMMENT'):
        requests.post(apiUrl + '/comment', json={'cmd':cmd, 'username':c[1], 'post_id':c[2], 'comment':c[3]})
    elif(cmd == 'FRIEND_REQUEST'):
        requests.post(apiUrl + '/friend_request', json={'cmd':cmd, 'from_user':c[1], 'to_user':c[2]})


def readInputFile(fileName):
    with open(fileName, "r") as f:
        for line in f:
            line = line.strip().rstrip()
            createCommand(line)

if __name__ =="__main__":
    fileName = sys.argv[1]
    start = time.perf_counter()
    readInputFile(fileName)
    stop = time.perf_counter()
    print("time taken:", stop - start)