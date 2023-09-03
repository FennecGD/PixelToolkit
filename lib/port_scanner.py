import queue
import socket
from threading import Thread, Lock
from queue import Queue

N_THREADS = 150

queue = Queue()
print_lock = Lock()

def scan_port(host, port):
    try:
        sock = socket.socket()
        sock.connect((host, port))
    except:
        pass
    else:
        with print_lock:
            print(f"{host:15}:{port:5} is open")
    finally:
        sock.close()


def scan_thread(host):
    global queue
    while True:
        port_number = queue.get()
        scan_port(host, port_number)
        queue.task_done()


def manage_port_scan(host, ports):
    global queue
    print("test")
    for thread in range(N_THREADS):
        thread = Thread(target=scan_thread, args=(host,))
        # if daemon is True that thread will end when the main threadends
        thread.daemon = True
        thread.start()

    for port in ports:
        # put each port to queue to start scan
        queue.put(port)

    queue.join()
