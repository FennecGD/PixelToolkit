from lib.utils import log, LogUrgency
import ipaddress
import re
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
    # print(host)
    for port in range(t_port_start, t_port_end + 1):
        if scan_port(host, port):
            results.append(f"{host} : {port}")


def scan_ip_range(lower_address, upper_address, n_threads, step, start, end, results):
    threads = []
    # print(upper_address, type(upper_address))
    for ip_int in range(lower_address, upper_address + 1):
        host = ipaddress.IPv4Address(ip_int)

        for i in range(n_threads):
            thread_start = start + i * step
            thread_end = start + (i + 1) * step - 1 if i != n_threads - 1 else end
            thread = threading.Thread(
                target=scan_thread, args=(str(host), thread_start, thread_end, results)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()


def scan_port_range(host, start_port, end_port, n_threads):
    # log(f"Port scanning started. host={host} range={start_port}-{end_port} n_threads={n_threads}", LogUrgency.INFO)
    results = []
    start, end = start_port, end_port
    step = (end - start + 1) // n_threads

    address_regex = r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$"

    if '-' in host:
        [lower_address, upper_address] = host.split("-")
        start_ip = ipaddress.IPv4Address(lower_address)
        end_ip = ipaddress.IPv4Address(upper_address)
        start_int = int(start_ip)
        end_int = int(end_ip)

        if not (re.match(address_regex, lower_address) and re.match(address_regex, upper_address)):
            log("Incorrect input data", LogUrgency.ERROR)

        else:
            scan_ip_range(start_int, end_int, n_threads, step, start, end, results)

    elif not re.match(address_regex, host):
        log("Incorrect input data", LogUrgency.ERROR)

    threads = []

# Convert the IP addresses to integers
    return results
