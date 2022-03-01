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
 
int main(void)
{
	// // void *ret;
	// pthread_t id;  
    // pthread_create(&id, NULL, threadFunc, NULL);  
	// // pthread_join(id, &ret);
	// pthread_detach(id);
	// sleep(1);
	string str1, str2;
	while(cin >> str1){
		str2 += str1 + ' ';
		if(cin.get() == '\n')break;
	}
	cout << "max:" << str2 << endl;
    return 0;
}
