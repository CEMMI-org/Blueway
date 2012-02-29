__author__ = 'mDan'

MODES = ["FILE","WEB","LIVE","GAME"]

class CONFIG:
     # general settings
     mode = 1 # 0=render to file,1=websocket, 2=live to lights, 3=pygame
     disableColormap = True

     #sim settings
     openbrowser = True

     #file mode settings
     pageRefresh = 0

     #web socket settings
     hostname = 'localhost'
     listen_port = '8000'

     #live settings
     subnet='10.32.0.{0}'

     #pygame setting
     scale = 2 # None or 1 for smaller
     margin = 10
     
     @staticmethod
     def getMode():
          return MODES[CONFIG.mode]

N = 50
M = 24

dt = 0.005
mapping = [1,3,2,4]#,11,10,7,5,3,4,13,16,15,14,9,12,8,6,24,23,21,22,18,20,17,19]
Ds = ['12','13']#,'5','6','12','13','14','36','19','20','15','16']
