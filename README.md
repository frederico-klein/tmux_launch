# tmux_launch

This is a replacement for roslaunch that instead divides the launch files into windows and panes depending on how many nodes you have. 

It's useful for debugging things and now I don't need to setup my custom yaml files that generate launch files and stuff, which was quite complicated, so this is nicer. 

I haven't tested it almost at all: it worked once and i decided to commit it. 

It also opens like a lot of unnecessary panes currently. I gotta improve that. 


## Usage

You have to first source the scripts/register_tmux.bash like:

    $ source scripts/register_tmux.bash

And add either the scripts directory or the /catkin_ws/devel/lib directory to your path like:

    $ export PATH=$PATH:/catkin_ws/devel/lib

Then if you type tmux_launch, it should autocomplete like roslaunch. 
