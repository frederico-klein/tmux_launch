#!/usr/bin/env python3

import subprocess
import tkinter as tk
from time import sleep
import libtmux
import rospy
import encodings
import traceback

window_dic_ ={"aaaa":["echo 1","echo 2", "echo 3"],
        "bbbb":["echo 4","echo 5"]}

start_directory="/catkin_ws/src/ros_biomech"

class TmuxManager:
    def __init__(self,session_name="test", first_window_name="roscore", load_env={}):
        self.name = session_name
        self.created_windows = []
        self.srv = libtmux.Server()
        self.default_window_name = first_window_name
        self.load_env = load_env
        self.session = None
        self.is_main_manager = None
        rospy.logwarn_once(load_env)
        if len(self.srv.sessions) == 0:
            self.is_main_manager = True
            return
        self.is_main_manager = False
        for a_session in self.srv.sessions:
            if a_session.name == self.name:
                self.session = a_session
        ## this doesnt work
        #self.srv.cmd('set-option' ,'-g', 'default-shell', '"/usr/bin/bash","--rcfile","~/.bashrc_ws.sh"')
    def create_session(self, session_name=None, initial_command=None, do_initial_split=True):
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
        self.close_pane = self.session.active_pane
        if do_initial_split:
            self.close_pane = self.session.active_window.split_window(vertical=True)
        #self.close_pane.send_keys("rosrun tmux_session_core close_tmux_button.py", enter=True)
        self.is_main_manager = True

    def new_tab(self,window_name=""):
        if self.is_main_manager and len(self.srv.sessions) == 0:
            self.create_session()
        my_new_window = self.session.new_window(window_name, start_directory=start_directory)
        self.created_windows.append(my_new_window)
        return my_new_window
    def attach(self):
        self.srv.cmd('-2','a','-t',self.name)
        #self.srv.attach_session(self.name)
    def newsplit(self):

        self.session.cmd('split-window','-h')

    def default_splits2(self,num=0, window_handle = None):

        if not window_handle:
            window_handle = self.session.windows[num]

        pane0 = window_handle.active_pane.split_window()

        return window_handle

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
        if self.srv.sessions:
            rospy.loginfo("Closing all windows")
            for w in self.created_windows:
                if not w:
                    continue
                for p in w.panes:
                    p.send_keys("C-c", enter=True)
                    ## I hope it will close eventually...
                w.kill()

    def kill_session(self):
        self.close_own_windows()
        if self.session and self.srv.sessions:
            rospy.loginfo("Attempting to kill own session")
            self.session.kill_session()

    ##def __del__(self):
    def cleanup(self):
        if self.is_main_manager:
            self.kill_session()
        else: ## then I just want to kill the windows I have created
            self.close_own_windows()

        #rospy.loginfo("Goodbye!")
        

def create_some_windows(window_dic={},some_manager=TmuxManager()):
    try:
        k = len(some_manager.session.windows)
        for i, (keys, values) in enumerate(window_dic.items()):
            pp = some_manager.new_tab(keys)
            if len(values) == 1:
                pass
            elif len(values) ==2:
                some_manager.default_splits2(window_handle=pp)
            elif len(values) <=4:
                some_manager.default_splits4(window_handle=pp)
            else:
                some_manager.default_splits8(window_handle=pp)
            #print(pp)

            if type(values) == type(""):
                rospy.logwarn("I was expecting a list, but got a string. I will assume you want only one command in this window.\nNote: you should write it down as a list because I need to know beforehand how many commands are going to be executed in this window, so I can divide it properly!")

                values = [values]
            if type(values) != type(list()):
                rospy.logerr("The syntax for this dictionary is a bit weird, for each window (the key), I am expecting a list of commands which are going to be exectuted.")
                raise Exception(f"Wrong type used for window commands. I was expecting a list, not {type(values)}")
            for j,cmd in enumerate(values):
                #print(cmd)
                rospy.loginfo("loading the part that should load the envs!"+str(some_manager.load_env))
                for keys, values in some_manager.load_env.items():
                    pp.panes[j].send_keys(f"export {keys}={values}", enter=True)
                pp.panes[j].send_keys(cmd, enter=True)

        pp.select()
    except:
        traceback.print_exc()

if __name__ == "__main__":
    print("being executed!")
    a = TmuxManager()
    a.create_session("test")
    create_some_windows(window_dic=window_dic_,some_manager=a)
    a.attach()
    #root.mainloop()


