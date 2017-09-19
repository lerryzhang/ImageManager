import hashlib
import random
import  datetime
class rutil:
   def md5(self,str):
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()
   def  getNewFileName(self,filename):
        suffix=filename.rsplit('.', 1)[1]
        randoms=random.randint(1000,9999)
        newFileName= '%s%s%s%s%s%s%s%s%s' % (datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,datetime.datetime.now().hour,datetime.datetime.now().minute,datetime.datetime.now().second,randoms,'.',suffix)
        return newFileName
