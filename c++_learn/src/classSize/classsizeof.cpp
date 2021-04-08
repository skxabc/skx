#include <iostream>
using namespace std;
class Animal
{
    public:
        Animal(){}
        ~Animal(){}
         
        //  virtual void func(){};
        // virtual void fun1(){};
        // virtual void fun2(){};
        int m_weight;

};
class test
{
    public:
        test(){};
        ~test(){};
        int test_b;
        // virtual void func1(){};
};
class Bird: virtual public Animal,virtual public test
{
    public:
        Bird(){}
        ~Bird(){}
        // virtual void func3(){};
};

class Horse:virtual public Animal
{
    public:
        Horse(){}
        ~Horse(){}
};
class FlyHorse:virtual public Horse,virtual public Bird
{
    public:
        FlyHorse(){}
        ~FlyHorse(){}
};
int main(char argv, char **args)
{
    Animal a;
    cout << "a: "<< sizeof(a) << endl;
    test t;
    cout << "t: " << sizeof(t) << endl;
    Bird b;
    cout << "b: "<< sizeof(b) << endl;
    // Horse h;
    // cout << "h: "<< sizeof(h) << endl;
    // FlyHorse fh;
    // fh.m_weight = 200;
    // cout << "fh: "<< sizeof(fh) <<endl;
    return 0;
}