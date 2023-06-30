// 这个宏保证 memleak.cpp 中的new 不会被memleak.hpp中的 宏替换 替换掉 test.cpp中不定义此宏，保证
//能被重载的new运算符替换，从而达到测试目的
#define NEW_OVERLOAD_IMPLEMENTATION

#include<iostream>
#include<cstring>
#include"memleak.hpp"


size_t LeakDetector::_callCount = 0;

// 我们使用带头节点的双向链表来手动管理内存申请与释放, 头节点的_prev指向最后一个结点, _next指向第一个结点
// 双向链表结构
typedef struct MemoryList{
    struct MemoryList* _prev;
    struct MemoryList* _next;
    size_t _size;
    bool _isArray;
    char* _file;
    size_t _line;
} MemoryList;

static MemoryList memoryListHead = {
    &memoryListHead, 
    &memoryListHead, 
    0,
    false,
    nullptr,
    0
};

static size_t memoryAllcated = 0;

void *AllcateMemory(size_t size, bool array, char* file, size_t line){
     size_t newSize = size + sizeof(MemoryList);
     MemoryList* newElem = (MemoryList*)malloc(newSize);

     newElem->_prev = &memoryListHead;
     newElem->_next = memoryListHead._next;
     newElem->_size = size;
     newElem->_isArray = array;

     if(nullptr != file){
        newElem->_file = (char*)malloc(strlen(file)+1);
        strncpy(newElem->_file, file, strlen(file) + 1);
     }else{
        newElem->_file = nullptr;
     }
     newElem->_line = line;

     memoryListHead._next->_prev = newElem;
     memoryListHead._next = newElem;

     memoryAllcated += size;
     return (char*)newElem + sizeof(memoryListHead);
}

void DeleteMemory(void *ptr, bool array){
    MemoryList* curElem = (MemoryList *)((char*)ptr - sizeof(MemoryList));
    if(curElem->_isArray !=  array) return;

    curElem->_next->_prev = curElem->_prev;
    curElem->_prev->_next = curElem->_next;

    memoryAllcated -= curElem->_size;
    if(nullptr != curElem->_file){
        free(curElem->_file);
    }

    free(curElem);
}

void *operator new(size_t size, char *file, size_t line){
    return AllcateMemory(size, false, file, line);
}

void* operator new[](size_t size, char* file, size_t line){
    return AllcateMemory(size, true, file, line);
}

void operator delete(void* ptr){
    DeleteMemory(ptr, false);
}

void operator delete[](void* ptr){
    DeleteMemory(ptr, true);
}

void LeakDetector::_LeakDetector(){
    if(0 == memoryAllcated){
        std::cout<<"congratulations, your code has not mem leak!"<<std::endl;
        return;
    }

    size_t count = 0;
    MemoryList* ptr = memoryListHead._next;
    while(nullptr != ptr && (&memoryListHead != ptr)){
        if(true == ptr->_isArray){
            std::cout<<"new[] doesn't release";
        }else{
            std::cout<<"new doesn't release";
        }
        std::cout<<"ptr:"<<ptr<<"size:"<<ptr->_size;

        if(nullptr != ptr->_file){
            std::cout<<"位于"<< ptr->_file<<"第"<<ptr->_line<<"行";
        }else{
            std::cout<<"无文件信息";
        }
        std::cout<<std::endl;
        ptr=ptr->_next;
        ++count;
    }
    std::cout<<"存在"<<count<<"处内存泄露，共包括"<<memoryAllcated<<"byte."<<std::endl;
    return;
}