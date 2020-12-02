#! /usr/bin/env python
import os
import numpy as np

spawnCommand = "./spawn_blue_box.sh "

j = 25
n = 0

def spawn_horizontal(j):
    i = 23
    global n
    while(i > -25):
        x = i + 0.5
        y = j + 0.5
        buff = spawnCommand + "Box" + str(n) + " " + str(x) + " " + str(y)
        os.system(buff)
        n += 1
        i -= 2

def spawn_vertical(i):
    j = 25
    global n
    while(j > -26):
        x = i + 0.5
        y = j + 0.5
        buff = spawnCommand + "Box" + str(n) + " " + str(x) + " " + str(y)
        os.system(buff)
        n += 1
        j -= 2

spawn_horizontal(25)
spawn_horizontal(-25)
spawn_vertical(25)
spawn_vertical(-25)