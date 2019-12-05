// Copyright 2019 Haoyu Xu xhy@bu.edu
#include <iostream>
#include <vector>
#include <string>
#include <math.h>
#include <sstream>
using namespace std;

class spheres {
public:
    double mass;
    double radius;
    vector<double> velocity;
    vector<double> position;
    string name;
    double count;
    double container;
    double bounces;
};

vector<double> add(vector<double> a, vector<double> b) {
    vector<double> v;
    v.push_back(a.at(0) + b.at(0));
    v.push_back(a.at(1) + b.at(1));
    v.push_back(a.at(2) + b.at(2));
    return v;
}

vector<double> substract(vector<double> a, vector<double> b) {
    vector<double> v;
    v.push_back(a.at(0) - b.at(0));
    v.push_back(a.at(1) - b.at(1));
    v.push_back(a.at(2) - b.at(2));
    return v;
}

vector<double> mul(vector<double> a, double b) {
    vector<double> v;
    v.push_back(a.at(0) * b);
    v.push_back(a.at(1) * b);
    v.push_back(a.at(2) * b);
    return v;
}

vector<double> div(vector<double> a, double b) {
    vector<double> v;
    v.push_back(a.at(0) / b);
    v.push_back(a.at(1) / b);
    v.push_back(a.at(2) / b);
    return v;
}

double dotproduct(vector<double> a, vector<double> b) {
    return a.at(0) * b.at(0) + a.at(1) * b.at(1) + a.at(2) * b.at(2);
}

double predictcollision(spheres s1, spheres s2) {
    double dx = s2.position.at(0) - s1.position.at(0);
    double dy = s2.position.at(1) - s1.position.at(1);
    double dz = s2.position.at(2) - s1.position.at(2);
    double dvx = s2.velocity.at(0) - s1.velocity.at(0);
    double dvy = s2.velocity.at(1) - s1.velocity.at(1);
    double dvz = s2.velocity.at(2) - s1.velocity.at(2);
    double a = pow(dvx, 2) + pow(dvy, 2)+ pow(dvz, 2);
    double b = 2 * (dx * dvx + dy * dvy + dz * dvz);
    double c = pow(dx, 2) + pow(dy, 2) + pow(dz, 2) - pow(s1.radius + s2.radius, 2) ;
    double d = pow(b, 2) - 4 * a * c;
    if (dotproduct(substract(s1.velocity, s2.velocity), substract(s1.position, s2.position)) >= 0) {
        return -1;
    }
    else if (d < 0) return -1;
    else if (a == 0) return -1;
    else if (d > 0) {
        double t1 = (-b + sqrt(d)) / (2 * a);
        double t2 = (-b - sqrt(d)) / (2 * a);
        if (t2 >= 0) {
            return t2;
        } else {
            return t1;
        }
    } else {
        return - b / (2 * a);
    }
}

double predictwall(spheres s1) {
    double a = pow(s1.velocity.at(0), 2) + pow(s1.velocity.at(1), 2) + pow(s1.velocity.at(2), 2);
    double b = 2 * s1.position.at(0) * s1.velocity.at(0) + 2 * (s1.position.at(1)) * (s1.velocity.at(1)) + 2 * (s1.position.at(2)) * (s1.velocity.at(2));
    double c = pow(s1.position.at(0), 2) + pow(s1.position.at(1), 2) + pow(s1.position.at(2), 2) - pow(s1.container - s1.radius, 2);
    double d = pow(b,2) - 4 * a * c;
    if (a == 0) {
        return -1;
    }
    if (d >= 0) {
        double t1 = (-b + sqrt(d)) / (2 * a);
        double t2 = (-b - sqrt(d)) / (2 * a);
        return max(t1, t2);
    }
    return -1;
}

vector<double> changev(spheres s1, spheres s2) {
    double m = (2 * s2.mass) / (s1.mass + s2.mass);
    vector<double> v = substract(s1.velocity, s2.velocity);
    vector<double> c = substract(s1.position, s2.position);
    vector<double> newvelocity = substract(s1.velocity, mul(c, dotproduct(v, c) * m / (dotproduct(c, c))));
    return newvelocity;
}

vector<double> wallchange(spheres s1) {
    double distance = sqrt(pow(s1.position.at(0), 2) + pow(s1.position.at(1), 2) + pow(s1.position.at(2), 2));
    vector<double> unit = div(s1.position, distance);
    vector<double> sproject = mul(unit, dotproduct(s1.velocity, unit));
    vector<double> soth = substract(s1.velocity, sproject);
    vector<double> newvelocity = substract(soth, sproject);
    return newvelocity;
}

void check(vector<spheres> spheres) {
    for (int i = 0; i < spheres.size(); i++) {
        if (spheres.at(i).count == -1) {
            cout << "disapper " << spheres.at(i).name << endl;
            spheres.erase(spheres.begin() + i);
        }
    }
    cout << "\n" << endl;
}

void outputInfo(vector<spheres> spheres) {
    vector<double> momentum;
    momentum.push_back(0);
    momentum.push_back(0);
    momentum.push_back(0);
    double energy = 0;
    for (auto & sphere : spheres) {
        momentum.at(0) += sphere.velocity.at(0) * sphere.mass;
        momentum.at(1) += sphere.velocity.at(1) * sphere.mass;
        momentum.at(2) += sphere.velocity.at(2) * sphere.mass;
        energy += 0.5 * sphere.mass * (pow(sphere.velocity.at(0), 2) +
                                       pow(sphere.velocity.at(1), 2) +
                                       pow(sphere.velocity.at(2), 2));
        cout << sphere.name << "m=" << sphere.mass << "R="
             << sphere.radius << "p=" << "(" << sphere.position.at(0)
             << "," << sphere.position.at(1) << "," << sphere.position.at(2)
             << ")" << "v=" << "(" <<sphere.velocity.at(0) << ","
             << sphere.velocity.at(1) << "," << sphere.velocity.at(2) << ")"
             << "bounces=" << sphere.bounces << endl;
    }
    cout << "momentum: " << "(" << momentum.at(0) << "," << momentum.at(1) << "," << momentum.at(2) << ")" << endl;
    cout << "energy: " << energy << endl;
    cout << "\n" << endl;
}

int main(int argc, char **argv) {
    vector<double> arg;
    vector<spheres> spheresname;
    if (argc == 1)
        exit(2);

    for (int i = 1; i < argc; i++) {
        if (stod(argv[i]) >= 0)
            arg.push_back(stod(argv[i]));
    }

    if (arg.empty())
        exit(2);

    double container = arg[0];
    int collision = arg[1];

    vector<string> row;
    vector<vector<string>> tables;
    string line;
    while (getline(cin, line)) {
        stringstream ss(line);
        string entry;
        while (ss >> entry) {
            row.push_back(entry);
        }
        tables.push_back(row);
        row.clear();
    }

    for (auto & table : tables) {
        if (table.size() != 9) {
            exit(1);
        }
        spheres name;
        name.mass = stod(table[0]);
        name.radius = stod(table[1]);
        name.position.push_back(stod(table[2]));
        name.position.push_back(stod(table[3]));
        name.position.push_back(stod(table[4]));
        name.velocity.push_back(stod(table[5]));
        name.velocity.push_back(stod(table[6]));
        name.velocity.push_back(stod(table[7]));
        name.name = table[8];
        name.count = collision;
        name.container = container;
        name.bounces = 0;
        spheresname.push_back(name);
    }

    cout << "Here are the initial conditions" << endl;
    cout << "universe radius " << container << endl;
    cout << "max collisions " << collision << endl;
    outputInfo(spheresname);
    cout << "Here are the events." << endl;
    cout << "\n" << endl;
    double sumtime = 0.0;
    vector<double> twoballs;
    vector<double> oneball;
    double time, wall;
    int sphere0, sphere1, sphere2;
    while (!spheresname.empty()) {
        twoballs.clear();
        oneball.clear();
        int stop = 0;
        for (auto & sphere : spheresname) {
            if (sphere.velocity.at(0) == 0 && sphere.velocity.at(1) == 0 && sphere.velocity.at(2) == 0) {
                stop++;
            }
        }
        if (stop == spheresname.size()) {
            break;
        }
        for (int i = 0; i < spheresname.size(); i++) {
            if (spheresname.at(i).count == -1) {
                spheresname.erase(spheresname.begin() + i);
            }
        }
        double mintime = 1.7976931348623157e+308;
        for (int i = 0; i < spheresname.size(); i++) {
            time = predictwall(spheresname.at(i));
            if (time == mintime) {
                oneball.push_back(i);
            }
            if (time < mintime && time > 0) {
                mintime = time;
                sphere0 = i;
                wall = mintime;
            }
        }
        mintime = 1.7976931348623157e+308;
        if (spheresname.size() > 1) {
            for (int i = 0; i < spheresname.size() - 1; i++) {
                for (int j = i + 1; j < spheresname.size(); j++) {
                    time = predictcollision(spheresname.at(i), spheresname.at(j));
                    if (time > 0 && time < mintime) {
                        mintime = time;
                        sphere1 = i;
                        sphere2 = j;
                    }
                }
            }
        }

        spheres temp;
        if (mintime < wall) {
            for (auto & sphere : spheresname) {
                sphere.position = add(mul(sphere.velocity, mintime), sphere.position);
            }
            spheresname.at(sphere1).count -= 1;
            spheresname.at(sphere2).count -= 1;
            spheresname.at(sphere1).bounces += 1;
            spheresname.at(sphere2).bounces += 1;
            temp = spheresname.at(sphere1);
            spheresname.at(sphere1).velocity = changev(spheresname.at(sphere1), spheresname.at(sphere2));
            spheresname.at(sphere2).velocity = changev(spheresname.at(sphere2), temp);
            sumtime += mintime;
            if (spheresname.at(sphere2).count > -1 || spheresname.at(sphere1).count > -1) {
                cout << "time of event " << sumtime << endl;
                cout << "colliding " << spheresname.at(sphere1).name << " " << spheresname.at(sphere2).name << endl;
                outputInfo(spheresname);
            }
            check(spheresname);
        } else {
            for (auto & sphere : spheresname) {
                sphere.position = add(mul(sphere.velocity, wall), sphere.position);
            }
            spheresname.at(sphere0).count -= 1;
            spheresname.at(sphere0).bounces += 1;
            spheresname.at(sphere0).velocity = wallchange(spheresname.at(sphere0));
            sumtime += wall;
            if (spheresname.at(sphere0).count > -1) {
                cout << "time of event: " << sumtime << endl;
                cout << "reflecting " << spheresname.at(sphere0).name;
                outputInfo(spheresname);
            }
            check(spheresname);
        }
    }
}