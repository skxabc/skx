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
// string make_lu(int cunt, const string &str, const string s="s"){
// 	return cunt > 1 ? str + s: str;
// }
// int f(int, int);
// std::vector<decltype(f)*> fVec;
// using f=int(int, int);
// vector<f*>fVec;
// usint f=int(*)(int, int);
// vector<f>fVec;
struct Sales_data
{
	string bookNo;
	unsigned units_sold = 0;
	double revenue = 0.0;
};
void test701()
{
	Sales_data total;
	if(cin>>total.bookNo>>total.units_sold>>total.revenue){
		Sales_data trans;
		while(cin>>trans.bookNo>>trans.units_sold>>trans.revenue){
			if(total.bookNo == trans.bookNo){
				total.units_sold += trans.units_sold;
				total.revenue += trans.revenue;
			}else{
				cout<<total.bookNo<<" "<<total.units_sold<<" "<<total.revenue<<endl;
				total = trans;
			}
		}
		cout<<total.bookNo<<" "<<total.units_sold<<" "<<total.revenue<<endl;
	}else{
		cerr<<"No data"<<endl;
	}
	return;
}
int main(void)
{
	test701();
	return 0;
}
