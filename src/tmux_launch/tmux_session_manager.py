#!/usr/bin/env python3

import subprocess
import tkinter as tk
from time import sleep
import libtmux
import rospy

window_dic_ ={"aaaa":["echo 1","echo 2", "echo 3"],
        "bbbb":["echo 4","echo 5"]}

start_directory="/catkin_ws/src/ros_biomech"

class TmuxManager:
    def __init__(self,session_name="test"):
        self.name = session_name
        self.created_windows = []
        self.srv = libtmux.Server()
        self.default_window_name = "roscore"
        ## this doesnt work
        #self.srv.cmd('set-option' ,'-g', 'default-shell', '"/usr/bin/bash","--rcfile","~/.bashrc_ws.sh"')
    def create_session(self, session_name=None, initial_command=None):
        #self.srv.cmd('new-session', '-d', '-P', '-F#{session_id}','-n',self.name).stdout[0]
        if session_name:
            self.name = session_name

        self.session = self.srv.new_session(self.name,start_directory=start_directory, window_name=self.default_window_name)
        if initial_command:
            rospy.loginfo("initial_command:%s"%initial_command)
            self.session.from_session_id
            self.session.active_window.active_pane.send_keys(initial_command, enter=True)
        else:
            rospy.logwarn_once("no initial command set")
        self.close_pane = self.session.active_window.split_window(vertical=True)
        #self.close_pane.send_keys("rosrun tmux_session_core close_tmux_button.py", enter=True)

    def new_tab(self,window_name=""):
        my_new_window = self.session.new_window(window_name, start_directory=start_directory)
        self.created_windows.append(my_new_window)
        return my_new_window
    def attach(self):
        self.srv.cmd('-2','a','-t',self.name)
        #self.srv.attach_session(self.name)
    def newsplit(self):

        self.session.cmd('split-window','-h')

    def default_splits4(self,num=0, window_handle = None):

        if not window_handle:
            window_handle = self.session.windows[num]

        pane0 = window_handle.active_pane
        pane1 = window_handle.split_window(vertical=True)
        pane2 = window_handle.split_window(vertical=True)
        pane3 = window_handle.split_window(vertical=True)


        pane0.cmd('select-layout','even-horizontal')
        return window_handle

    def default_splits8(self,num=0,window_handle = None):
        wh = self.default_splits4(num=num, window_handle=window_handle)
        for pane in wh.panes:
            pane.split_window()

        return wh

    def close_own_windows(self):
        for w in self.created_windows:
            w.kill()

    def kill_session(self):
        self.close_own_windows()
        self.session.kill_session()

def create_some_windows(window_dic={},some_manager=TmuxManager()):
    k = len(some_manager.session.windows)
    for i, (keys, values) in enumerate(window_dic.items()):
        some_manager.new_tab(keys)
        #a.newsplit()
        window_index = i+k
        pp = some_manager.default_splits8(num=window_index)
        #print(pp)

        for j,cmd in enumerate(values):
            #print(cmd)
            pp.panes[j].send_keys(cmd, enter=True)

    pp.select()

if __name__ == "__main__":
    print("being executed!")
    a = TmuxManager()
    a.create_session("test")
    create_some_windows(window_dic=window_dic_,some_manager=a)
    a.attach()
    #root.mainloop()


