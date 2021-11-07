/*
 * @lc app=leetcode.cn id=9 lang=cpp
 *
 * [9] 回文数
 */

// @lc code=start
class Solution {
public:
    bool isPalindrome(int x) {
        //负数直接返回false
        if(x < 0)
        {
            return false;
        }
        //正数转成string 两个指针相向而行，直到遇到
        string str = to_string(x);
        for(int beg = str.begin(),int end = str.end();beg < end; beg++,end--)
        {
            if(str[beg] != str[end])
            {
                return false;
            }
        }
        return true;   
    }
};
// @lc code=end

