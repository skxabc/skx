#include <iostream>
#include <fstream>
#include <stdio.h>
#include "Sales_item.h"
using namespace std;
int main()
{
    //read a group record of sales
    // fstream file;
    // file.open("/Users/shikaixun/Desktop/skx/c++_learn/src/cplusplusPrimer/testData/book_sales");
     freopen("/Users/shikaixun/Desktop/skx/c++_learn/src/cplusplusPrimer/testData/book_sales","r", stdin);
    // cout<< "errno" << errno << "descr:" << strerror(errno) <<endl;
    // // vector<Sales_item> saleRecord;
    // Sales_item book;
    // if(!file)cout << "open file failed" <<endl; 
    // // file >> book;
    // // cout << book << endl;
    // while(file.get()){
    //      cout << book << endl;
    // }
    Sales_item book;
    int i = 4;
    while(i--){
        cin >> book;
        cout << book << endl;
    }
    //output the record to the screen
    return 0;
}