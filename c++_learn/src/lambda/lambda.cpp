#include<iostream>
#include<algorithm>
//不用lambda函数
// void display(int a)
// {
//     std::cout<<a<<" ";
// }
// int main()
// {
//     int arr[]={1,2,3,4,5};
//     std::for_each(arr,arr + sizeof(arr)/sizeof(int),&display);
//     std::cout<<std::endl;
// }

using namespace std;
//使用不能引用外部变量的lambda函数
// int main()
// {
//     int arr[] = {1,2,3,4,5};
//     for_each(arr,arr+sizeof(arr)/sizeof(int),[](int a){cout<<a<<" ";});
//     cout << endl;
    
// }
//[=](int a){cout << a << " "}     "="表示外部变量值传递
//[&](int a){cout << a << " "}     "&"表示外部变量引用传递

//使用引用外部变量的lambda函数 外部变量值传递
int main()
{
    int arr[] = {1,2,3,4,5};
    int mul = 5;
    // for_each(arr, arr+sizeof(arr)/sizeof(int),[=](int a){mul = 3;cout << a << " mul:" << mul; });
    // [=]时，mul为只读，编译不过
    for_each(arr, arr+sizeof(arr)/sizeof(int),[&](int a){mul = 3;cout << a << " mul:" << mul; });
    // [&]时，可以修改外部变量，mul被改为3

    cout << endl;
}