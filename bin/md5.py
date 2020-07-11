import hashlib
import os
import datetime

def GetFileMd5(filename):
    if not os.path.isfile(file):
        return
    myhash = hashlib.md5()
    f = file(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()