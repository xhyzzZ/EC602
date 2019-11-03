#include <iostream>
#include <vector>
#include <string>
#include <math.h>
using namespace std; 


class spheres
{
public:
  float mass;
  float radius;
  std::vector<float> velocity;
  std::vector<float> position;
  string name;
  float count;
  float container;
};

vector<float> addv(vector<float> a,vector<float> b){
  std::vector<float> v;
  v.push_back(a.at(0)+b.at(0));
  v.push_back(a.at(1)+b.at(1));
  v.push_back(a.at(2)+b.at(2));
  return v;
}

vector<float> mulv(vector<float> a,vector<float> b){
  std::vector<float> v;
  v.push_back(a.at(0)*b.at(0));
  v.push_back(a.at(1)*b.at(1));
  v.push_back(a.at(2)*b.at(2));
  return v;
}


vector<float> subv(vector<float> a,vector<float> b){
  std::vector<float> v;
  v.push_back(a.at(0)-b.at(0));
  v.push_back(a.at(1)-b.at(1));
  v.push_back(a.at(2)-b.at(2));
  return v;
}

float dotproduct(vector<float> a,vector<float> b){
  return a.at(0)*b.at(0)+a.at(1)*b.at(1)+a.at(2)*b.at(2);
}

float predict(spheres s1,spheres s2){
  float a = pow(s1.velocity.at(0)-s2.velocity.at(0),2)+ pow(s1.velocity.at(1)-s2.velocity.at(1),2)+ pow(s1.velocity.at(2)-s2.velocity.at(2),2);
  float b = 2*(s1.position.at(0)-s2.position.at(0))*(s1.velocity.at(0) - s2.velocity.at(0))+ 2*(s1.position.at(1)-s2.position.at(1))*(s1.velocity.at(1) - s2.velocity.at(1))+ 2*(s1.position.at(2)-s2.position.at(2))*(s1.velocity.at(2) - s2.velocity.at(2));
  float c =pow(s1.position.at(0)-s2.position.at(0),2)+ pow(s1.position.at(1)-s2.position.at(1),2)+ pow(s1.position.at(2)-s2.position.at(2),2);
  float d = pow(b,2)-4*a*c;
  if (dotproduct(subv(s1.velocity,s2.velocity),subv(s1.position,s2.position))>= 0){
    return -1;
  }
  if (a==0){
    return -1;
  }
  float t1 = (-b + sqrt(d))/(2*a);
  float t2 = (-b - sqrt(d))/(2*a);
  return min(t1,t2);
}

float predictwall(spheres s1){
  float a = pow(s1.velocity.at(0),2)+ pow(s1.velocity.at(1),2)+ pow(s1.velocity.at(2),2);
  float b = 2*(s1.position.at(0))*(s1.velocity.at(0))+ 2*(s1.position.at(1))*(s1.velocity.at(1))+ 2*(s1.position.at(2))*(s1.velocity.at(2));
  float c =pow(s1.position.at(0),2)+ pow(s1.position.at(1),2)+ pow(s1.position.at(2),2);
  float d = pow(b,2)-4*a*c;
  if (a==0){
    return -1;
  }
  if (d>=0){
    float t1 = (-b + sqrt(d))/(2*a);
    float t2 = (-b - sqrt(d))/(2*a);
    return max(t1,t2);
  }
}

vector<float> mulnv(vector<float> a,float b){
  std::vector<float> v;
  v.push_back(a.at(0)*b);
  v.push_back(a.at(1)*b);
  v.push_back(a.at(2)*b);
  return v;
}

vector<float> divnv(vector<float> a,float b){
  std::vector<float> v;
  v.push_back(a.at(0)/b);
  v.push_back(a.at(1)/b);
  v.push_back(a.at(2)/b);
  return v;
}


vector<float> changev(spheres s1,spheres s2){
  float m = (2*s2.mass)/(s1.mass + s2.mass);
  vector<float> v = subv(s1.velocity,s2.velocity);
  vector<float> c = subv(s1.position,s2.position);
  vector<float> newvelocity = subv(s1.velocity,mulnv(c,dotproduct(v,c)*m/(dotproduct(c,c))));
  return newvelocity;
}

vector<float> wallchange(spheres s1){
  float distance = sqrt(pow(s1.position.at(0),2)+pow(s1.position.at(1),2) + pow(s1.position.at(2),2));
  vector<float> unit = divnv(s1.velocity,distance);
  vector<float> sproject = mulv(mulv(s1.velocity,unit),unit);
  std::vector<float> soth = subv(s1.velocity,sproject);
  vector<float> newvelocity = subv(soth,sproject);
  return newvelocity;
}


int main(int argc,char** argv){
  float container = stoi(*(argv+1));
  float collision = stoi(*(argv+2));
  std::vector<spheres> spheresname;
  float mass,rad,p1,p2,p3,v1,v2,v3;
  string name,i;
  while (cin >> mass >> rad >> p1 >> p2 >> p3 >> v1 >> v2 >> v3 >> name){
    i = name;
    spheres name;
    name.mass = mass;
    name.radius = rad;
    name.velocity.push_back(v1);
    name.velocity.push_back(v2);
    name.velocity.push_back(v3);
    name.position.push_back(p1);
    name.position.push_back(p1);
    name.position.push_back(p1);
    name.name = i;
    name.container = container;
    name.count = collision;
    spheresname.push_back(name);
  }
  float energy;
  vector<float> momentum;
  momentum.push_back(0);
  momentum.push_back(0);
  momentum.push_back(0);
  for(int i = 0; i != spheresname.size(); i++){
    energy += 0.5* spheresname.at(i).mass*(pow(spheresname.at(i).velocity.at(0),2)+pow(spheresname.at(i).velocity.at(1),2)+pow(spheresname.at(i).velocity.at(2),2));
    momentum.at(0) += spheresname.at(i).velocity.at(0)*spheresname.at(i).mass;
    momentum.at(1) += spheresname.at(i).velocity.at(1)*spheresname.at(i).mass;
    momentum.at(2) += spheresname.at(i).velocity.at(2)*spheresname.at(i).mass;
  }
  cout << "here are the initial sphere" << endl;
  for(int i = 0; i != spheresname.size(); i++){
    cout << spheresname.at(i).name << 'm =' << spheresname.at(i).mass << 'r ='<< spheresname.at(i).radius <<'p ='<<spheresname.at(i).position.at(0)<<spheresname.at(i).position.at(1)<<spheresname.at(i).position.at(2)<<'v ='<<spheresname.at(i).velocity.at(0)<<spheresname.at(i).velocity.at(1)<<spheresname.at(i).velocity.at(2)<<endl;
  }
  cout <<'energy' << energy<<endl;
  cout << 'momentum' << momentum.at(0)<<momentum.at(1)<<momentum.at(2)<<endl;
  float sumtime = 0.0;
  float time,wall;
  int sphere0,sphere1,sphere2;
  while (spheresname.size()>0){
    float mintime = 99999999.0;
    for (int i= 0; i<spheresname.size();i++){
      time = predictwall(spheresname.at(i));
      if ((time < mintime)&& (time > 0)){
        mintime = time;
        sphere0 = i;
        wall = mintime;
      }
    }
    for (int i = 0; i<spheresname.size()-1;i++ ){
      for (int j = i+1; j<spheresname.size();j++){
        if ((time > 0) && (time < mintime)){
          mintime = time;
          sphere1 = i;
          sphere2 = j;
        }
      } 
    }
    std::vector<float> mm;
    spheres temp;
    if (mintime < wall){
      for(int i = 0; i < spheresname.size();i++){
        mm = addv(mulnv(spheresname.at(i).velocity,mintime),spheresname.at(i).position);
        spheresname.at(i).position = mm;
      }
      spheresname.at(sphere1).count -= 1;
      spheresname.at(sphere2).count -= 1;
      temp = spheresname.at(sphere1);
      spheresname.at(sphere1).velocity = changev(spheresname.at(sphere1),spheresname.at(sphere2));
      spheresname.at(sphere2).velocity = changev(spheresname.at(sphere2),temp);
      sumtime += mintime;
      if (spheresname.at(sphere2).count !=0 || spheresname.at(sphere1).count != 0){
        cout << 'time of event' << sumtime << endl;
        cout <<'colliding' << spheresname.at(sphere1).name << spheresname.at(sphere2).name;
        cout << spheresname.at(sphere1).name << 'm =' << spheresname.at(sphere1).mass << 'r ='<< spheresname.at(sphere1).radius <<'p ='<<spheresname.at(sphere1).position.at(0)<<spheresname.at(sphere1).position.at(1)<<spheresname.at(sphere1).position.at(2)<<'v ='<<spheresname.at(sphere1).velocity.at(0)<<spheresname.at(sphere1).velocity.at(1)<<spheresname.at(sphere1).velocity.at(2)<<endl;
        cout << spheresname.at(sphere2).name << 'm =' << spheresname.at(sphere2).mass << 'r ='<< spheresname.at(sphere2).radius <<'p ='<<spheresname.at(sphere2).position.at(0)<<spheresname.at(sphere2).position.at(1)<<spheresname.at(sphere2).position.at(2)<<'v ='<<spheresname.at(sphere2).velocity.at(0)<<spheresname.at(sphere2).velocity.at(1)<<spheresname.at(sphere2).velocity.at(2)<<endl;
        cout <<'energy' << energy;
        cout << 'momentum' << momentum.at(0)<<momentum.at(1)<<momentum.at(2)<<endl;
      }
    }
    else{
      for(int i = 0; i < spheresname.size();i++){
        mm = addv(mulnv(spheresname.at(i).velocity,wall),spheresname.at(i).position);
      }
      spheresname.at(sphere0).count -= 1;
      spheresname.at(sphere0).velocity = wallchange(spheresname.at(sphere0));
      sumtime += wall;
      if (spheresname.at(sphere0).count != 0){
        cout << 'time of event' << sumtime << endl;
        cout <<'colliding' << spheresname.at(sphere0).name;
        cout << spheresname.at(sphere0).name << 'm =' << spheresname.at(sphere0).mass << 'r ='<< spheresname.at(sphere0).radius <<'p ='<<spheresname.at(sphere0).position.at(0)<<spheresname.at(sphere0).position.at(1)<<spheresname.at(sphere0).position.at(2)<<'v ='<<spheresname.at(sphere0).velocity.at(0)<<spheresname.at(sphere0).velocity.at(1)<<spheresname.at(sphere0).velocity.at(2)<<endl;
        cout <<'energy' << energy;
        cout << 'momentum' << momentum.at(0)<<momentum.at(1)<<momentum.at(2)<<endl;
      }
    for(int i = 0; i < spheresname.size();i++){
      if (spheresname.at(i).count == 0){
        spheresname.erase(spheresname.begin()+i);
      }
    }
    }
  }
}