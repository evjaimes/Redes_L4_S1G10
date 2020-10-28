import socket
from socketserver import ThreadingMixIn
import logging
from datetime import date
from datetime import datetime
from protocol import ProtocolThread

'''
SERVER PROCESS
'''

# _HOST = socket.gethostbyaddr("<your-ec2-public_ip>")[0] #  --> AMAZON EC2 IP
_HOST = 'localhost'
_PORT = 1813
_MAX_CONNECTIONS = 25




if __name__ == "__main__":
    logging.basicConfig(filename='.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)
    cad = f'\n\n{date.today().strftime("%B %d, %Y")} - {datetime.now().strftime("%H:%M:%S")}\n'
    logging.info(cad)

    UDP_Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDP_Sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    UDP_Sock.bind((_HOST, _PORT))
    threads = []
    try:
        while True:
            #máximo de conecciones es 25
            logging.info(f'--> Listening on {_HOST}:{_PORT}')
            print(f'--> Listening on {_HOST}:{_PORT}')
            address = UDP_Sock.recvfrom(1024)
            logging.info(
                f'+ --> [Server] Connection Established with Client {address}')
            print(f'+ --> [Server] Connection Established with Client {address}')
            new_thread = ProtocolThread(address[0],address[1])
            new_thread.execute()
            threads.append(new_thread)
        
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("\n--> [Server End] Caught Keyboard Interrupt.\n--> Exiting\n ")
    

    
