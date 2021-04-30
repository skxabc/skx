// @before-stub-for-debug-begin
#include <vector>
#include <string>
#include "commoncppproblem7.h"

using namespace std;
// @before-stub-for-debug-end

/*
 * @lc app=leetcode.cn id=7 lang=cpp
 *
 * [7] 整数反转
 */

// @lc code=start
class Solution {
public:
    
    int reverse(int x) {
        int ret = 0;
        int tmp = 0;
        while(x != 0)
        {
            tmp = x%10;
            if(ret > 214748364 || (ret == 214748364 && tmp > 7)) return 0;
            if(ret < -214748364 || (ret == -214748364 && tmp < -8)) return 0;
            ret = ret*10 + tmp;
            x = x/10;
        }
        return ret;
    }
};
// @lc code=end
/*1032/1032 cases passed (0 ms)
Your runtime beats 100 % of cpp submissions
Your memory usage beats 64.88 % of cpp submissions (5.8 MB)
*/