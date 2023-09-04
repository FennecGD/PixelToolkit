import socket
import threading
from queue import Queue

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


def scan_thread(host, thread_start, thread_end):
    for port in range(thread_start, thread_end + 1):
        scan_port(host, port)


def start_port_scan(host, ports_range, n_threads):
    start, end = ports_range[0], ports_range[-1]    
    step = (end - start + 1) // n_threads

    threads = []
    for i in range(n_threads):
        thread_start = start + i * step
        thread_end = start + (i + 1) * step - 1 if i != n_threads - 1 else end
        thread = threading.Thread(target=scan_thread, args=(host, thread_start, thread_end))
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()
