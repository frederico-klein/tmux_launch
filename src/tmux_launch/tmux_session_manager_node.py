#!/usr/bin/env python3

import rospy
from acquisition_of_raw_data.tmux_session_manager import *


if __name__ == "__main__":
    rospy.init_node("tmux_session_manager")
    rospy.loginfo("does it work")
    session_name =  rospy.get_param("~session_name","test")
    initial_command =  rospy.get_param("~initial_cmd","")
    myManager = TmuxManager(session_name)
    myManager.create_session(initial_command=initial_command)
    myManager.attach()
    rospy.spin()
