import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/winicon/octavia_ws/src/RobotControl_ws/install/robots_nav_contr'
