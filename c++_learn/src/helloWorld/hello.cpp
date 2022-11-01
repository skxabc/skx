#include<iostream>
#include <string.h>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <iostream>
#include <future>
#include <chrono>
 
std::promise<int> promis;
int main(int argc, const char * argv[]) {
    std::future<int> fuResult = promis.get_future();
    std::thread t([](){
        std::this_thread::sleep_for(std::chrono::seconds(1));
        promis.set_value(123);
    });
    t.detach();
    std::cout<<"detach..."<<std::endl;
    std::cout<<fuResult.get()<<std::endl;
    return 0;
}
