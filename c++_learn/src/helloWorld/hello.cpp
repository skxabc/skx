#include<iostream>
#include <string.h>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
using namespace std;
 
// void* threadFunc(void* p)  
// {  
// 	char szTest[1024 * 32] = {0};
//     return NULL;  
// }  
string make_lu(int cunt, const string &str, const string s="s"){
	return cunt > 1 ? str + s: str;
}
int f(int, int);
std::vector<decltype(f)*> fVec;
using f=int(int, int);
vector<f*>fVec;
usint f=int(*)(int, int);
vector<f>fVec;
int main(void)
{
	// void *ret;
	// pthread_t id;  
    // pthread_create(&id, NULL, threadFunc, NULL);  
	// // pthread_join(id, &ret);
	// pthread_detach(id);
	// sleep(1);
	string a = "apple";
	string b = "peek";
	cout<<make_lu(2,a)<<endl;
	cout<<make_lu(1,b)<<endl;
    return 0;
}
