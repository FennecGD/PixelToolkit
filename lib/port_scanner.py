import socket
import threading
from queue import Queue
from lib.utils import Color

queue = Queue()


def scan_port(host, port):
    try:
        sock = socket.socket()
        sock.connect((host, port))
        RESET = Color.RESET
        GREEN = Color.GREEN
        GRAY = Color.GRAY
        BLUE = Color.BLUE
        print(f"[{GREEN}+{RESET}] {GRAY}({host}){RESET}\tOpen port: {BLUE}{port}{RESET}")
    except:
        pass
    finally:
        sock.close()


def scan_thread(host, t_port_start, t_port_end):
    for port in range(t_port_start, t_port_end + 1):
        scan_port(host, port)


def scan_port_range(host, start_port, end_port, n_threads):
    start, end = start_port, end_port
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

    print(f"[{Color.LIGHT_GREEN}!{Color.RESET}] Port scan finished")
