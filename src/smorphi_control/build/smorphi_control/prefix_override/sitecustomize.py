import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/alicia/rbrz_ws/src/smorphi_control/install/smorphi_control'
