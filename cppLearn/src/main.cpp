#include <iostream>
#include <string>
#include <vector>
using namespace std;
int main(int argv, char **agrv)
{
    vector<int>obj;
    for(int i = 0; i<10; ++i)
    {
        obj.push_back(i);
        cout<<obj[i]<<",";
    }
    for(int i=0; i < 5; ++i)
    {
        obj.pop_back();
    }
     
    cout<<"\n"<<endl;
    for(int i = 0; i< obj.size(); ++i)
    {
        cout<<obj[i]<<",";
    }
    return 0;
}
