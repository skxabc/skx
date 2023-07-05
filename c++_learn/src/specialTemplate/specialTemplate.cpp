#include <iostream>
#include <cstring>
using namespace std;

//function template 
template<class T>
int compare(const T& l, const T& r){
    cout<<"in template<class T>..."<<endl;
    return l-r;
}

//function template special
//template <>
int compare(const char* l, const char* r){
    cout<<"in special template<>..."<<endl;
    return strcmp(l, r);
}

//class template
template<class T>
class Compare
{
    public:
    static 
}
int main(int argc, char** argv)
{
    compare(1,2);
    const char* l = "";
    const char* r = "";
    compare(l,r);
    return 0;
}