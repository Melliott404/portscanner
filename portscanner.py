import socket
import threading
import sys
from queue import Queue

# target = the host you would like to scan (the target below is the nmap host we have permission to scan)
# open_ports = a list for all of the open ports found after scan
target = "45.33.32.156"
queue = Queue()
open_ports = []

# The portscan itself
def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False
    
#  If true, port number will be saved to open_port list
def fill_queue(port_list):
    for port in port_list:
        queue.put(port)

# Grabs the next port number to scan when the queue is empty
def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print("Port {} is open.".format(port))
            open_ports.append(port)

# The specific ports or range of ports chosen to scan
port_list = range(1, 1025)
fill_queue(port_list)

thread_list = []

# Allows the scan to use more threads resulting in a faster scan. # is adjustable
for t in range(500):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()

# Saves the reference of the standard output
original_stdout = sys.stdout

# Writes the open ports from the target host to a log file, any new scans will be appended to the file (change file to desired location)
with open('portscanner_logs.txt', 'a') as f:
    sys.stdout = f
    print("Open ports on", target, "are:", open_ports)

# Resets the standard output to print the scan done in the command line
    sys.stdout = original_stdout

# Prints a list of all the open ports found on the targeted host on the command line
print("Open ports on", target, "are:", open_ports)
