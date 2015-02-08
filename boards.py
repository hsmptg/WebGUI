import threading
import socket

class Raspi(object):
    def __init__(self, parent=None):
        self.onMsg = None   
    
    def connect(self, ip, port):
        self._exit = False
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        try:
            self.soc.connect((ip, port))
            self.th = threading.Thread(target = self._th_read)
            self.th.start()
            return True            
        except Exception,e:
            print str(e)
            return False
  
    def sendCmd(self, cmd):
        try:
            self.soc.sendall(cmd + '\r\n')
        except AttributeError:
            print('Not connected yet!')
        except socket.error:
            print('Lost connection!')        

    def _th_read(self):
        buf = ""
        self.soc.settimeout(1)
        while not self._exit:
            try:
                dat = self.soc.recv(1024)
                if dat == "":
                    print("Disconnected")
                    break # if conn lost get out!
                buf = buf + dat
                while "\r\n" in buf: # PuTTY send CR+LF per each "Enter" key
                    (cmd, buf) = buf.split("\r\n", 1)
                    if self.onMsg and cmd<>"":
                        self.onMsg(cmd)                        
            except socket.timeout:
                #print("timeout")
                continue
            except socket.error:
                print('Lost connection!')
                break            

    def disconnect(self):
        self._exit = True
        self.th.join()
        self.soc.close()
    
class Duino(object):
    def __init__(self, parent=None):
        self.onMsg = None   
    
    def connect(self, port):
        self._exit = False
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        try:
#            self.soc.connect((ip, port))
            self.th = threading.Thread(target = self._th_read)
            self.th.start()
            return True            
        except Exception,e:
            print str(e)
            return False
  
    def sendCmd(self, cmd):
        try:
            self.soc.sendall(cmd + '\r\n')
        except AttributeError:
            print('Not connected yet!')
        except socket.error:
            print('Lost connection!')        

    def _th_read(self):
        buf = ""
        self.soc.settimeout(1)
        while not self._exit:
            try:
                dat = self.soc.recv(1024)
                if dat == "":
                    print("Disconnected")
                    break # if conn lost get out!
                buf = buf + dat
                while "\r\n" in buf: # PuTTY send CR+LF per each "Enter" key
                    (cmd, buf) = buf.split("\r\n", 1)
                    if self.onMsg and cmd<>"":
                        self.onMsg(cmd)                        
            except socket.timeout:
                #print("timeout")
                continue
            except socket.error:
                print('Lost connection!')
                break            

    def disconnect(self):
        self._exit = True
        self.th.join()
        self.soc.close()
    