#include <string>
#include <iostream>
#include <fstream>
using namespace std;
typedef struct base_t{
    int64_t a;
    int64_t b;
}stBase_t;
int main(){
    int *p = new int;
    cout << "p val:"<<p<<endl;
    stBase_t *test = (stBase_t *)p;
    cout << "test.a addr:" << &(test->a) << endl;
    cout << "test.a val:" << test->a <<endl;

    cout <<"test.b addr:"<<&(test->b)<<endl;
    cout <<"test.b val:" << test->b <<endl;
    return 0;
}

// int main(int argc, char **argv)
// {
//     ofstream filetest;
//     filetest.open("skxcppfiletest.txt",ios::trunc);
//     filetest<<"sxiaowei"<<'\n';
//     filetest<<"yangyuan"<<'\n';
//     return 0;    
// }

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

 
