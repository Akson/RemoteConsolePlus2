'''
Created on Oct 20, 2013

@author: Dmytro
'''
from RCP2Client.RCP2Client import RCP2Client
import time

if __name__ == '__main__':
    rc = RCP2Client()
    rc.Connect("tcp://127.0.0.1:55557")
    
    i=0
    while True:
        rc.SendMessage("test%d"%(i))
        i+=1
        time.sleep(0.1)