import sys
import os
from pySmartDL import SmartDL

url = sys.argv[1]
dest = os.getcwd()

obj = SmartDL(url, dest)
obj.start()
# [*] 0.23 Mb / 0.37 Mb @ 88.00Kb/s [##########--------] [60%, 2s left]

path = obj.get_dest()