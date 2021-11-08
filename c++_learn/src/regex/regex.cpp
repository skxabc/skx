#include<regex>
#include<iostream>

using namespace std;
int main()
{
    //遍历文件每一行
    // ifstream dwake("./dwakeConfig")
    // bool foundmatch = false;
    // try {
    	// std::regex re(R"(\b\w+(?=\=)|=.+)");
        
    	// foundmatch = std::regex_search(subject, re);
    // } catch (std::regex_error& e) {
    	// Syntax error in the regular expression
    // }
    std::cmatch m;
    regex r("\\w+=(.*)");
    auto ret = std::regex_match("BOARD_TYPE=1", m, r);
    if(ret){
        cout<<m.str()<< endl;
        cout<<m.length()<<endl;
        cout<<m.position()<<endl;
    }
    cout<<"----------------------"<<endl;
    for(int i = 0; i < m.size(); i++){
        cout <<m[i].str()<<endl;
    }
    return 0;
}

/*output:
BOARD_TYPE=1
12
0
----------------------
BOARD_TYPE=1
1
*/