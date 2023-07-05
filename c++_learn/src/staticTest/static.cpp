#include <iostream>
using namespace std;
    class Pet{
    public:
        Pet(string name);
        ~Pet();
        static int getcount();  
    protected:
        string thename;

    private:
        static int count;
    };

    class Dog :public Pet
    {
    public:
        Dog(string name);
    };
    class Cat :public Pet{
    public:
        Cat(string name);
    };

    int Pet::count = 0;
 
 Pet::Pet(string name){
    thename = name;
    count++;
    cout<<"one pet be born, name is:"<<thename<<endl;
 }
 Pet::~Pet(){
    count--;
    cout<<thename<<"dead!"<<endl;
 }
 int Pet::getcount(){
    return count;
 }

 Dog::Dog(string name):Pet(name){

 }

 Cat::Cat(string name):Pet(name){

 }

 int main(){
    Dog dog("WangCai");
    Cat cat("Penny");
    cout<<"has already"<<Pet::getcount()<<"puppy"<<endl;
    return 0;
 }

