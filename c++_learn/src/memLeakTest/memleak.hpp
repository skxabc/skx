#ifndef LEAK_DETECTOR_H_
#define LEAK_DETECTOR_H_
#include <stddef.h>
void *operator new(size_t size, char *file, size_t line);
void *operator new[](size_t size, char *file, size_t line);

void operator delete(void *ptr);
void operator delete[](void *ptr);

#ifndef NEW_OVERLOAD_IMPLEMENTATION 
#define new new(__FILE__, __LINE__)
#endif

class LeakDetector{
public:
    static size_t _callCount;
    LeakDetector(){ ++_callCount; }
    ~LeakDetector(){ 
        if(0 == --_callCount){
            _LeakDetector();
        }
     }
private:
    void _LeakDetector();
};

static LeakDetector exitCounter;

#endif