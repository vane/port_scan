import sys
import socket
import concurrent.futures
import os
from itertools import repeat

# start end port
start_port=1
end_port=65535
# timeouts in seconds - maximum of time to spent on one port is sum of this list
socket_timeouts=[.5, 1]
# concurrency level
thread_number=200

timed_out_error = 'timed out'
# ignored errors
known_errors = ['[Errno 61] Connection refused', timed_out_error]

recv_open_ports = dict()
send_open_ports = dict()
recv_possible_ports = dict()
send_possible_ports = dict()


def scan_port(*args):
    port, address = args[0]
    if port % 1000 == 0:
        print(f'scanning {port}')
    for timeout in socket_timeouts:
        result = open_recv_port(port, address, timeout)
        if result:
            break
    for timeout in socket_timeouts:
        result = open_send_port(port, address, timeout)
        if result:
            break


def open_send_port(port, address, timeout):    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((address, port))
        data = sock.send(b'\n\n')
        # print(f'send {port}:{data}')
        sock.close()
        send_open_ports[address].add(port)
        print(f'send open {address} {port}')        
    except Exception as e:
        s = str(e)
        if s == timed_out_error:
            return False
        # TODO if timeout scan once more but increse timeout 
        if s not in known_errors:
            print(f'send problem {port} {s}')
            send_possible_ports[address].add((port, s))
    return True


def open_recv_port(port, address, timeout):    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((address, port))
        data = sock.recv(2048)
        # print(f'recv {port}:{data}')
        sock.close()
        recv_open_ports[address].add((port, data))
        print(f'recv open {address} {port}')
    except Exception as e:
        s = str(e)
        if s == timed_out_error:
            return False
        # TODO if timeout scan once more but increse timeout 
        if s not in known_errors:
            print(f'recv problem {port} {s}')
            recv_possible_ports[address].add((port, s))
    return True


def scan_address_list(address_list):
    for address in address_list:      
        recv_open_ports[address] = set()
        send_open_ports[address] = set()
        recv_possible_ports[address] = set()
        send_possible_ports[address] = set()

        if os.path.exists(f'{address}.txt'):    
            print(f'File exists {address}.txt skipping')
            continue

        port_range = list(range(start_port, end_port))
        print(f'start scan {address} port range {port_range[0]}:{port_range[-1]} test timeouts: {socket_timeouts}')
        
        with concurrent.futures.ThreadPoolExecutor(thread_number) as executor:
            executor.map(scan_port, zip(port_range, repeat(address)))
        
        result = f'''complete scan {address} port range {port_range[0]}:{port_range[-1]} test timeouts: {socket_timeouts}
send open ports {list(recv_open_ports[address])}
recv open ports {list(send_open_ports[address])}
send possible ports {list(send_possible_ports[address])}
recv possible ports {list(recv_possible_ports[address])}
'''
        with open(f'{address}.txt', 'w+') as f:
            f.write(result)
        print(result)

if __name__ == '__main__':
    scan_address_list(sys.argv[1].split(','))
