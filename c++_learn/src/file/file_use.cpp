#include <string>
#include <iostream>
#include <fstream>
#include <unistd.h>
using namespace std;
typedef struct base_t{
    int64_t a;
    int64_t b;
}stBase_t;
<<<<<<< HEAD
int main(){
    int *p = new int;
    cout << "p val:"<<p<<endl;
    stBase_t *test = (stBase_t *)p;
    cout << "test.a addr:" << &(test->a) << endl;
    cout << "test.a val:" << test->a <<endl;

    cout <<"test.b addr:"<<&(test->b)<<endl;
    cout <<"test.b val:" << test->b <<endl;
    return 0;
=======
// int main(){
//     int *p = new int;
//     cout << "p val:"<<p<<endl;
//     stBase_t *test = (stBase_t *)p;
//     cout << "test.a addr:" << &(test->a) << endl;
//     cout << "test.a val:" << test->a <<endl;
// }
int main(int argc, char **argv)
{
    // ofstream filetest;
    // filetest.open("skxcppfiletest.txt",ios::trunc);
    // filetest<<"sxiaowei"<<'\n';
    // filetest<<"yangyuan"<<'\n';
    int i = 0;
    while(true){
        sleep(10);
        if(i == 0){
            int * p = new int[16];
        }
        cout<<"index: "<<++i<< endl;
    }
    return 0;    
>>>>>>> d68f195c1ed9cf10faca87eb604d5f9ba6a4eca5
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

 
