#!/usr/bin/env python3

import rospy
from tmux_launch.tmux_session_manager import *
import signal
import sys
import os

def signal_handler(manager_object, sig, frame):
    manager_object.cleanup()
    rospy.signal_shutdown("Shutdown via CTRL-C")
    sys.exit(0)

def cleanup_args(args):
    line = ''
    new_args = []
    for arg in args:
        if arg[0] == '_':
            continue
        line+= f' {arg}'
        new_args.append(arg)
    return line, new_args

if __name__ == "__main__":
    rospy.init_node("tmux_neovim", anonymous=True)
    rospy.loginfo("does it work")
    append_args, new_args = cleanup_args(sys.argv[1:])
    #rospy.loginfo(sys.argv)
    #rospy.loginfo(append_args)
    session_name =  rospy.get_param("~session_name","testtt")
    initial_command =  rospy.get_param("~initial_cmd","nv")
    myManager = TmuxManager(session_name)
    #myManager.create_session(initial_command=initial_command)
    tab_name = "editor"
    path = os.path.abspath(".")
    if len(new_args)>1:
        tab_name = os.path.basename(new_args[0])
    a_window = myManager.new_tab(window_name=tab_name)
    complete_command = f"cd {path} && {initial_command}{append_args}"
    a_window.active_pane.send_keys(complete_command, enter=True)
    #myManager.attach()
     # Capture CTRL-C
    signal.signal(signal.SIGINT, lambda x, y: signal_handler(myManager,x,y))
    rospy.spin()
