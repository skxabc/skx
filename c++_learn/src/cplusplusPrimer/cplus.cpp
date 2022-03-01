#include <iostream>
#include <fstream>
#include <stdio.h>
#include <string>
// #include "Sales_item.h"
#include "Sales_data.h"
using namespace std;


int main()
{
    Sales_data data1, data2;
    double price = 0;
    cin >> data1.bookNo >> data1.units_sold >> price;
    data1.revenue = data1.units_sold * price;
    cin >> data2.bookNo >> data2.units_sold >> price;
    data2.revenue = data2.units_sold * price;
    
    if(data1.bookNo == data2.bookNo){
        unsigned totalCnt = data1.units_sold + data2.units_sold;
        double totalRevenue = data1.revenue + data2.revenue;
         
        cout << data1.bookNo << " " << totalCnt << " " << totalRevenue << " ";

        if(totalCnt != 0){
            cout << totalRevenue/totalCnt << endl;
        }else{
            cout<< "(no sales)" << endl;
        }
    }else{
        cerr << "data must be refer to the same ISBN" << endl;
        return -1;
    }
    return 0;
}