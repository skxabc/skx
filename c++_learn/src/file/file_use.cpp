#include <string>
#include <iostream>
#include <fstream>
using namespace std;

int main(int argc, char **argv)
{
    ofstream filetest;
    filetest.open("skxcppfiletest.txt",ios::trunc);
    filetest<<"sxiaowei"<<'\n';
    filetest<<"yangyuan"<<'\n';
    return 0;    
}

// int main()
// {
//     // char buf[256];
//     // FILE* file = fopen("./test.txt", "r");
//     // fgets(buf, 5, file);
//     // printf("buf:%s\n",buf);
//     char *a = "hello";
//     string b = a;
//     cout<<"strlen(a):"<<b.length()<<endl;
//     return 0;
// }