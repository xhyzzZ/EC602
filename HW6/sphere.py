#  Copyright 2019 zeyu song zeyusong@bu.edu
import sys
import numpy as np 
import math  

class Sphere():
  def __init__(self,sphere,max_collision,container_radius):
    self.mass = float(sphere[0])
    self.radius = float(sphere[1])
    self.velocity = np.array([float(i) for i in sphere[5:8]])
    self.name = sphere[8]
    self.current = np.array([float(i) for i in sphere[2:5]])
    self.count = float(max_collision)
    self.container = float(container_radius)



  # def move(self):
  #   #detect if sphere reach edge of container
  #   self.current += self.velocity
  #   other.current += other.velocity
  #   dis = (self.current[0]**2 + self.current[1]**2 + self.current[2]**2)**-2
  #   if dis >= self.container:
  #     self.velocity = -self.velocity
  #     self.count -= 1
  #   co = (self.current - other.current)
  #   n = np.dot(co,co)
  #   if n <= (self.radius+self.radius)**2:
  #     self.count -= 1
  #     self.velocity= self.velocity - np.multiply(np.dot(np.subtract(self.velocity,other.velocity),np.subtract(self.current,other.current)),(2*other.mass)/(self.mass + other.mass)/np.dot(self.current-other.current,self.current-other.current),(self.current-other.current))\
  #     ,other.velocity - np.multiply(np.dot(np.subtract(other.velocity,self.velocity),np.subtract(other.current,self.current)),(2*self.mass)/(self.mass + other.mass)/np.dot(other.current-self.current,other.current-self.current)*(other.current-self.current))

def changev(s1,s2):
  m = (2*s2.mass)/(s1.mass + s2.mass)
  v = np.subtract(s1.velocity,s2.velocity)
  cc = []
  for i in range(len(s1.current)):
    cc.append(s1.current[i] - s2.current[i])
  c = np.array(cc)
  newvelocity = np.subtract(s1.velocity,np.multiply(np.dot(v,c)*m/(np.dot(c,c)),c))
  return newvelocity

def wallchange(s1):
  distance = math.sqrt(s1.current[0]**2 + s1.current[1]**2 + s1.current[2]**2)
  unit = s1.current/distance
  sproject = s1.velocity*unit*unit
  soth = s1.velocity - sproject
  newvelocity = -sproject + soth
  return newvelocity

def predict(s1,s2):
  a = (s1.velocity[0]-s2.velocity[0])**2 + (s1.velocity[1]-s2.velocity[1])**2 + (s1.velocity[2]-s2.velocity[2])**2
  b = 2*(s1.current[0] -s2.current[0])*(s1.velocity[0]-s2.velocity[0]) + 2*(s1.current[1] -s2.current[1])*(s1.velocity[1]-s2.velocity[1]) + 2*(s1.current[2] -s2.current[2])*(s1.velocity[2]-s2.velocity[2])
  c = (s1.current[0]-s2.current[0])**2 + (s1.current[1]-s2.current[1])**2 + (s1.current[2]-s2.current[2])**2 -(s1.radius + s2.radius)**2
  d = b**2 -4*a*c
  if np.dot(np.subtract(s1.velocity,s2.velocity),np.subtract(s1.current,s2.current)) >=0:
    return -1
  if a == 0:
    return -1
  if d == 0:
    return (-b+math.sqrt(b**2 -4*a*c))/(2*a)
  elif d > 0:
    t1 = (-b+math.sqrt(b**2 -4*a*c))/(2*a)
    t2 = (-b-math.sqrt(b**2 -4*a*c))/(2*a)
    if t1 > 0 and t2 >0:
      return min(t1,t2)
    elif t1>0 or t2>0:
      return max(t1,t2)
    else:
      return -1
  else :
    return -1

def predictwall(s1):
  a = s1.velocity[0]**2 + s1.velocity[1]**2 + s1.velocity[2]**2
  b = 2*s1.velocity[0]*s1.current[0]+2*s1.velocity[1]*s1.current[1]+2*s1.velocity[2]*s1.current[2]
  c = s1.current[0]**2 + s1.current[1]**2 + s1.current[2]**2 - (s1.container-s1.radius)**2
  if a == 0:
    return -1
  d = b**2 -4*a*c
  if d >= 0:
    t1 = (-b+math.sqrt(b**2 -4*a*c))/(2*a)
    return (t1)
  else:
    return -1


def main():
  #get input
    container_radius = sys.argv[1]
    max_collision = sys.argv[2]
    data = sys.stdin.readlines()
    sphere = [[] for _ in range(len(data))]
    m= 0 
    for line in data:
      line = line.strip('\n')
      line = line.split(' ')
      for i in line:
        sphere[m].append(i)
      m += 1
    spherename = []
    for i in range(m):
      sphere[i][8] = Sphere(sphere[i],max_collision,container_radius)
      spherename.append(sphere[i][8])
    energy = 0
    momentum = np.array([0,0,0])
    #initial output
    for i in spherename:
      energy += 0.5*i.mass*(i.velocity[0]**2+i.velocity[1]**2+i.velocity[2]**2)
      momentum = np.add(momentum,np.multiply(i.velocity,i.mass))
    print('here are the initial sphere')
    for i in spherename:
      print(i.name,'m = ',i.mass,'R = ',i.radius,'p = ',i.current,'v = ',i.velocity)
    print('energy:',energy)
    print('momentum:',momentum)
    timesum = 0 
    while len(spherename) > 0:
      mintime = 9999999999999999999
      for i in range(len(spherename)):
        time = predictwall(spherename[i])
        if time < mintime and time > 0:
          mintime = time
          wall = mintime
          sphere0 = i
      for i in range(len(spherename)-1):
        for j in range(i+1,len(spherename)):
          time = predict(spherename[i],spherename[j])
          if time > 0 and time < mintime:
            mintime = time
            sphere1 = i
            sphere2 = j
      if mintime < wall:
        for i in spherename:
          m = np.add(i.current, np.multiply(i.velocity,mintime))
          i.current = m
        spherename[sphere1].count -= 1
        spherename[sphere2].count -= 1
        spherename[sphere1].velocity,spherename[sphere2].velocity= changev(spherename[sphere1],spherename[sphere2]),changev(spherename[sphere2],spherename[sphere1])
        timesum += mintime
        if spherename[sphere2].count != 0 or spherename[sphere1].count != 0:
          print('time of event:',timesum)
          print('colliding',spherename[sphere1].name,spherename[sphere2].name)
          print(spherename[sphere1].name,'m = ',spherename[sphere1].mass,'R = ',spherename[sphere1].radius,'p = ',tuple(spherename[sphere1].current),'v = ',tuple(spherename[sphere1].velocity))
          print(spherename[sphere2].name,'m = ',spherename[sphere2].mass,'R = ',spherename[sphere2].radius,'p = ',tuple(spherename[sphere2].current),'v = ',tuple(spherename[sphere2].velocity))
          print('energy:',energy)
          print('momentum:',momentum)
      else:
        for i in spherename:
          i.current = np.add(i.current, np.multiply(i.velocity,wall))
        spherename[sphere0].count -= 1
        spherename[sphere0].velocity = wallchange(spherename[sphere0])
        timesum +=wall
        if spherename[sphere0].count != 0:
          print('time of event:',timesum)
          print('colliding',spherename[sphere0].name)
          print(spherename[sphere0].name,'m = ',spherename[sphere0].mass,'R = ',spherename[sphere0].radius,'p = ',tuple(spherename[sphere0].current),'v = ',tuple(spherename[sphere0].velocity))
          print('energy:',energy)
          print('momentum:',momentum)
      for i in spherename:
        if i.count == 0:
          spherename.remove(i)
if __name__ == '__main__':
  main()