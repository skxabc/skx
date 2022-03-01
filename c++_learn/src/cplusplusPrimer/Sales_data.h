#ifndef SALESDATA_H
#define SALESDATA_H
using namespace std;
struct Sales_data 
{
    string bookNo;
    unsigned  units_sold = 0;
    unsigned int cost;
    double revenue = 0.0;
};
#endif