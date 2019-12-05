// Copyright 2018 J Carruthers 
// Version 2.0
//

#include <iostream>
#include <chrono>
#include <string>
#include <vector>

using namespace std::chrono;
using std::string;

class Timer {
 public:
  Timer();
  Timer(string,bool silence=false);
  ~Timer();
  void start();
  void stop();


 duration<double> total_time;
 high_resolution_clock::time_point tstart;
 string name;
 bool running;
 bool silent;
 int count;

 double time() {
 	if (!running)
     return total_time.count();

    high_resolution_clock::time_point t2 = high_resolution_clock::now();

    duration<double> t = duration_cast<duration<double>>(t2 - tstart);
   return t.count();
}
} ;

Timer::Timer() {
  count = 0;
  total_time = duration<double>::zero();
  name = "overall";
  running = true;
  silent = false;
  start();
}

Timer::Timer(string s,bool silence) {
  count = 0;
  total_time = duration<double>::zero();
  name = s;
  running = false;
  silent = silence;
}


void Timer::start() {
  tstart = high_resolution_clock::now();
  running = true;
}

void Timer::stop() {
  high_resolution_clock::time_point t2 = high_resolution_clock::now();

  total_time += duration_cast<duration<double>>(t2 - tstart);
  running = false;
}

Timer::~Timer() {
  if (running)
    stop();

  if (not silent) {
    std::cerr << "timer " << name << " " << total_time.count() << '\n';
  }
}


const int LIMIT = 300'000'000;
const double MYTIME = 0.048;


double computer_speed() {
  // returns how much faster your computer is than the server
  // 2.5 means your time was 2.5 times less than the server time.
  Timer t("calibrate",true);
  t.start();
  int total = 0;
  for (int i=0; i<LIMIT;i++)
    total += i;
  t.stop();
  std::cerr << "total is " << total << " calculated in " << t.time() << " seconds\n";
  return MYTIME/t.time();
}