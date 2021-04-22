#include <string>
#include <iostream>
#include <fstream>
using namespace std;
int main(int argc, char **argv)
{
    ofstream filetest;
    filetest.open("skxcppfiletest.txt",ios::trunc);
    filetest<<"shikaixun"<<'\n';
    filetest<<"haoyue"<<'\n';
    return 0;    
}