#!/usr/bin/env python

import socket, signal, sys, json, os

database_file = os.path.join(os.getcwd(), 'database', 'database.json')
current_reads_file = "reads.json"

# Given a list of non-unique rfid epcs as input, this will return a list containing only unique epcs
def find_uniques(data_in):
    data_list = []
    for datum in data_in.split('\n'):
        datum = datum.rstrip().upper()
        if datum not in data_list and len(datum) > 0:
            data_list.append(datum)
    return data_list
    
# Reads file passed as input into a python dict representing the JSON structure of the file and returns the dict
def get_database(database_file_in):
    with open(database_file_in, 'r') as f:
        return json.loads(f.read())
    
# Compares present read epcs to entries in full database and returns the subset of the database which matches the present read epcs
def construct_json(tag_list_in, database_in):
    json_list = []

    for entry in database_in['RFID Data List']:
        if str(entry['ID Number']) in tag_list_in:
            json_list.append(entry)
            
    with open(current_reads_file, 'w') as f:
        json.dump({'RFID Data List': json_list}, f)
        
    return json.dumps({'RFID Data List': json_list})

# Ctrl-c handler
def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    print "Releasing socket"
    signal.signal(signal.SIGINT, original_sigint)
    
    if (conn != 0):
        conn.close()
    sys.exit(1)

    # restore the exit gracefully handler here    
    signal.signal(signal.SIGINT, exit_gracefully)

if __name__ == "__main__":
    database = get_database(database_file)
    
    # store the original SIGINT handler for ctrl-c handling
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

    # Define parameters for tcp connection
    TCP_IP = '192.168.1.117'
    TCP_PORT = 60001
    BUFFER_SIZE = 1405  
    conn = socket._socketobject() # Instantiate dummy conn variable in case ctrl-c is pressed before actual connection is established
    
    # Open tcp connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow for the socket to be reused
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    
    # While loop to receive data through tcp connection until ctrl-c is pressed
    while 1:
        # Wait to accept incoming connection from Wifly
        conn, addr = s.accept()
        print 'Connection address:', addr

        while 1:
            # M6e is hardcoded to time out if not enough reads occur in 10 seconds
            data = conn.recv(BUFFER_SIZE)
            # If timeout occurred, construct an empty JSON object and break loop to reconnect
            if not data:
                construct_json("", database)
                break 
            #print "data:", data
            received_tags = find_uniques(data)
            print "received data:", received_tags          
            construct_json(received_tags, database)
            
        conn.close()
