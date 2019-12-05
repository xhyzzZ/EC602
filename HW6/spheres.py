#!/usr/bin/python
# Copyright 2019 Haoyu Xu xhy@bu.edu
import sys
import numpy as np
import math

class Sphere():
    def __init__(self, sphere, max_collision, container_radius, bounces):
        self.mass = float(sphere[0])
        self.radius = float(sphere[1])
        self.name = sphere[8]
        self.velocity = np.array([float(i) for i in sphere[5:8]])
        self.current = np.array([float(i) for i in sphere[2:5]])
        self.count = int(max_collision)
        self.container = float(container_radius)
        self.bounces = bounces

def changev(s1, s2):
    M = (2 * s2.mass) / (s1.mass + s2.mass)
    dv = np.subtract(s1.velocity, s2.velocity)
    dp = np.subtract(s1.current, s2.current)
    newvelocity = np.subtract(s1.velocity, np.multiply(np.dot(dv, dp) * M / (np.dot(dp, dp)), dp))
    return newvelocity

def wallchange(s1):
    distance = math.sqrt(s1.current[0] ** 2 + s1.current[1] ** 2 + s1.current[2] ** 2)
    unit = s1.current / distance
    sproject = np.array(np.multiply(np.dot(s1.velocity, unit), unit))
    soth = s1.velocity - sproject
    newvelocity = -sproject + soth
    return newvelocity

def predict(s1, s2):
    dx = s2.current[0] - s1.current[0]
    dy = s2.current[1] - s1.current[1]
    dz = s2.current[2] - s1.current[2]
    dvx = s2.velocity[0] - s1.velocity[0]
    dvy = s2.velocity[1] - s1.velocity[1]
    dvz = s2.velocity[2] - s1.velocity[2]
    a = dvx ** 2 + dvy ** 2 + dvz ** 2
    b = 2 * (dx * dvx + dy * dvy + dz * dvz)
    c = dx ** 2 + dy ** 2 + dz ** 2 - (s1.radius + s2.radius) ** 2
    d = b ** 2 - 4 * a * c
    if np.dot(np.subtract(s1.velocity, s2.velocity), np.subtract(s1.current, s2.current)) >= 0:
        return -1
    if a == 0:
        return -1
    if d < 0:
        return -1
    elif d > 0:
        s1 = (- b + math.sqrt(d)) / (2 * a)
        s2 = (- b - math.sqrt(d)) / (2 * a)
        return s2 if s2 >= 0 else s1
    else :
        return - b / (2 * a)

def predictwall(s1):
    a = s1.velocity[0] ** 2 + s1.velocity[1] ** 2 + s1.velocity[2] ** 2
    b = 2 * s1.velocity[0] * s1.current[0] + 2 * s1.velocity[1] * s1.current[1] + 2 * s1.velocity[2] * s1.current[2]
    c = s1.current[0] ** 2 + s1.current[1] ** 2 + s1.current[2] ** 2 - (s1.container - s1.radius) ** 2
    if a == 0:
        return -1
    d = b ** 2 - 4 * a * c
    if d >= 0:
        t1 = (-b + math.sqrt(d)) / (2 * a)
        t2 = (-b - math.sqrt(d)) / (2 * a)
        return max(t1, t2)
    else:
        return -1
def outputinfo(spherename):
    momentum = np.array([0,0,0])
    energy = 0
    for i in spherename:
        energy += 0.5 * i.mass * (i.velocity[0] ** 2 + i.velocity[1] ** 2 + i.velocity[2] ** 2)
        momentum = np.add(momentum, np.multiply(i.velocity, i.mass))
        print('{} m={} R={} p={} v={} bounces={}'.format(i.name, i.mass, i.radius, tuple(i.current), tuple(i.velocity), i.bounces))
    print('energy: {}'.format(energy))
    print('momentum: {}'.format(tuple(momentum)))
    print()

def check_and_remove(spherename):
    for i in spherename:
        if i.count == -1:
            print('disappear {}'.format(i.name))
            print
            spherename.remove(i)
    print()

def main():
    container_radius = float(sys.argv[1])
    max_collision = int(sys.argv[2])
    data = sys.stdin.readlines()
    sphere = [[] for _ in range(len(data))]
    index = 0
    for line in data:
        line = line.strip('\n')
        line = line.split()
        for i in line:
            sphere[index].append(i)
        index += 1
    spherename = []
    for i in range(index):
        sphere[i][8] = Sphere(sphere[i], max_collision, container_radius, 0)
        spherename.append(sphere[i][8])

    print('Here are the initial sphere')
    print('universe radius {}'.format(container_radius))
    print('max collisions {}'.format(max_collision))
    outputinfo(spherename)
    print('Here are the events.')
    print()
    sum_of_time = 0
    while len(spherename) > 0:
        stop = 0
        for i in spherename:
            if i.velocity[0] == 0 and i.velocity[1] == 0 and i.velocity[2] == 0:
                stop += 1
        if stop == len(spherename):
            print(spherename)
            break
        for i in spherename:
            if i.count == -1:
                spherename.remove(i)
        mintime = sys.float_info.max
        wall = sys.float_info.max
        wallcball = []
        twoballs = []
        for i in range(len(spherename)):
            time = predictwall(spherename[i])
            if time == mintime:
                wallcball.append(i)
            if time < mintime and time > 0:
                mintime = time
                wall = mintime
                wallcball = [i]
        mintime = sys.float_info.max
        for i in range(len(spherename) - 1):
            for j in range(i + 1, len(spherename)):
                time = predict(spherename[i], spherename[j])
                if time == mintime:
                    twoballs.append((i, j))
                if time > 0 and time < mintime:
                    mintime = time
                    twoballs = [(i, j)]
    
        if mintime < wall:
            for i in spherename:
                i.current = np.add(np.multiply(i.velocity, mintime), i.current)
            for i in range(len(twoballs)):
                spherename[twoballs[i][0]].count -= 1
                spherename[twoballs[i][1]].count -= 1
                spherename[twoballs[i][0]].bounces += 1
                spherename[twoballs[i][1]].bounces += 1
                spherename[twoballs[i][0]].velocity, spherename[twoballs[i][1]].velocity = changev(
                spherename[twoballs[i][0]], spherename[twoballs[i][1]]), changev(spherename[twoballs[i][1]],
                                                                                     spherename[twoballs[i][0]])
                sum_of_time += mintime
            for i, j in twoballs:
                if spherename[i].count > -1 or spherename[j].count != -1:
                    print('time of event: {}'.format(sum_of_time))
                    print('colliding {} {}'.format(spherename[i].name, spherename[j].name))
                    outputinfo(spherename)
            check_and_remove(spherename)
        else:
            for i in spherename:
                i.current = np.add(np.multiply(i.velocity, wall), i.current)
            for i in wallcball:
                spherename[i].count -= 1
                spherename[i].bounces += 1
                spherename[i].velocity = wallchange(spherename[i])
            sum_of_time += wall
            for i in wallcball:
                if spherename[i].count > -1:
                    print('time of event: {}'.format(sum_of_time))
                    print('reflecting {}'.format(spherename[i].name))
                    outputinfo(spherename)
            check_and_remove(spherename)
    
if __name__ == '__main__':
    main()
