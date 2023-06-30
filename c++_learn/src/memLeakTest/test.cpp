#include "memleak.hpp"

int main(int argc, char ** argv){
    int *a = new int;
    int* b = new int[12];
    // delete a;
    delete []b;
    return 0 ;
}