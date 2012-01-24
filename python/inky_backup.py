'''
Created on Jan 30, 2011

@author: NStevens
'''
from datetime import datetime, timedelta
import pickle

if __name__ == '__main__':
    try:
        ofile = open("C:\\backup\\lastbackup.dat","rb+")
        prevdatetime = pickle.load(ofile)
        ofile.close()
    except:
        prevdatetime = datetime.min
        
    cdatetime = datetime.now()
    print(prevdatetime)
    print(cdatetime)
    
    day = timedelta(days=1)
    if (abs(cdatetime - prevdatetime) > day):
        print("Greater!")
    else:
        print("Less!")
    
    ofile = open("C:\\backup\\lastbackup.dat","wb")
    pickle.dump(cdatetime, ofile)
    ofile.close()