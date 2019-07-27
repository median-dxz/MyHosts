import socket
import threading
routers = []
lock = threading.Lock()
barrier = threading.Barrier(25)
haveFind = False

def search_routers():
    global haveFind
    ip = '104.18.18.18'
    all_threads = []

    for i in range(16, 32):
        for j in range(0, 256):
            for k in range(1, 255):
                if (haveFind == True):
                    break
                array = ip.split('.')
                array[1] = str(i)
                array[2] = str(j)
                array[3] = str(k)
                new_ip = '.'.join(array)
                t = threading.Thread(target=check_ip, args=(new_ip,))
                t.start()
                all_threads.append(t)
    for t in all_threads:
        t.join()


def check_ip(new_ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((new_ip, 80))
    s.close()
    if result == 0:
        global haveFind
        haveFind = True
        lock.acquire()
        print(new_ip.ljust(15), 'is open')
        routers.append((new_ip, 80))
        lock.release()


print('Searching for routers, please wait...')
search_routers()
