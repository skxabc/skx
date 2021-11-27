#include<fstream>
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
    // std::cmatch m;
    // regex r("(\\w+)=(.*)");
    // auto ret = std::regex_match("BOARD_TYPE=1", m, r);
    // if(ret){
    //     cout<<m.str()<< endl;
    //     cout<<m.length()<<endl;
    //     cout<<m.position()<<endl;
    //     cout<<m.size()<<endl;
    // }
    // cout<<"----------------------"<<endl;
    // for(int i = 1; i < m.size(); i+=2){
    //     cout <<m[i].str()<<endl;
    //     cout <<m[i+1].str()<<endl;
    // }
    fstream file1("./test.txt");
    string line;
    while(getline(file1, line)) {
        printf("line:%s\n",line.c_str());
        cmatch m;
        regex r("(\\w+)=(.*)");
        auto ret = regex_match(line.c_str(), m, r);
        printf("m.size():%d\n",m.size());
        for(int i = 1; i < m.size(); i+=2){
            printf("%s",m[i].str());
            printf("=");
            printf("%s",m[i+1].str());
        }
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