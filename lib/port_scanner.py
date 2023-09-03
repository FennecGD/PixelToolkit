import socket
from threading import Thread
from queue import Queue
import multiprocessing

N_THREADS = multiprocessing.cpu_count()

queue = Queue()

def scan_port(host, port):
    try:
        sock = socket.socket()
        sock.connect((host, port))
        print(f"{host}\t{port:5} is open")
    except:
        pass
    finally:
        sock.close()


def scan_thread(host):
    global queue
    # TODO reimplement this loop with multiple ranges and threads
    while True:
        port_number = queue.get()
        scan_port(host, port_number)
        queue.task_done()


def start_port_scan(host, ports):
    global queue
    for thread in range(N_THREADS):
        thread = Thread(target=scan_thread, args=(host,))
        # if daemon is True that thread will end when the main threadends
        thread.daemon = True
        thread.start()

    for port in ports:
        # put each port to queue to start scan
        queue.put(port)

    queue.join()
