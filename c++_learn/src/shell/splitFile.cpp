#include <stream>

int main(int args, char **argv)
{
    const char crtPath[128]="/Users/shikaixun/Desktop/skx/c++_learn/src/shell/ca-certificates.crt";
    istream file(crtPath);
    string line;
    while(getline(file, line)){
        cout<<line<<endl;
        regex re("-----BEGIN CERTIFICATE-----[\s\S]-----END CERTIFICATE-----");
        cmatch mold;
    }
    return 0;

}