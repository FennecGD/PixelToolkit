import socket
import threading


def scan_port(host, port) -> bool:
    try:
        sock = socket.socket()
        sock.connect((host, port))
        sock.close()
        return True
    except:
        return False


def scan_thread(host, t_port_start, t_port_end, results):
    for port in range(t_port_start, t_port_end + 1):
        if scan_port(host, port):
            results.append(port)


def scan_port_range(host, start_port, end_port, n_threads):
    results = []
    start, end = start_port, end_port
    step = (end - start + 1) // n_threads

    threads = []
    for i in range(n_threads):
        thread_start = start + i * step
        thread_end = start + (i + 1) * step - 1 if i != n_threads - 1 else end
        thread = threading.Thread(
            target=scan_thread, args=(host, thread_start, thread_end, results)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results
