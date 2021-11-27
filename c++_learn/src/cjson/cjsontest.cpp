#include <iostream>
#include "cJSON.h"
#include <string.h>
#include <fstream>
using namespace std;
char txt[]="{\"shikaixun\":\"1\",\"haoyue\":\"3\"}";
int main()
{
    cJSON* json;
    cJSON* shi;
    cJSON* hao;
    cJSON* tmp;
    json = cJSON_Parse(txt);
    char test[256];
    strncpy(test,cJSON_PrintUnformatted(json),256);
    printf("test:%s",test);
    // printf("before:%s",json);
    // cJSON_Print(json);
    // printf("after:%s",cJSON_Print(json));
    // int num = cJSON_GetArraySize(json);
    // printf("num:%d\n",num);
        // tmp = json->child;
    // ofstream fileout("./testskx.txt");
    // for(int i = 0; i < num; i++){
        // printf("arr:%s",cJSON_Print(tmp));
        // tmp = tmp->next;三次握手

    // string s="/tmp/uaibot/";
    // if(s[s.length()-1] == '/'){
    //     printf("last simbol is:%c\n",s[s.length()-1]);
    //     s = s + "dwakeconfig";
    //     printf("path:%s\n",s.c_str());
    // }

    // if(!json){
    //     printf("err\n");
    // }else{

    //     shi = cJSON_GetObjectItem(json,"shikaixun");
    //     printf("shikaixun:%s\r\n",shi->valuestring);
    //     hao = cJSON_GetObjectItem(json,"haoyue");
    //     printf("haoyue:%s\r\n",hao->valuestring);
    //  }
}