#include<iostream>
#include <string.h>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <iostream>
#include <future>
#include <chrono>
 
<<<<<<< Updated upstream
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
=======
// void* threadFunc(void* p)  
// {  
// 	char szTest[1024 * 32] = {0};
//     return NULL;  
// }  
// string make_lu(int cunt, const string &str, const string s="s"){
// 	return cunt > 1 ? str + s: str;
// }
// int f(int, int);
// std::vector<decltype(f)*> fVec;
// using f=int(int, int);
// vector<f*>fVec;
// usint f=int(*)(int, int);
// vector<f>fVec;
void change(int *m){
	m = (int*)1;
}
int main(void)
{
	// test701();

	int *p = nullptr;
	change(p);
	cout<<"P:"<<p<<endl;
	return 0;
>>>>>>> Stashed changes
}
