/*
 * @lc app=leetcode.cn id=9 lang=cpp
 *
 * [9] 回文数
 * 给你一个整数 x ，如果 x 是一个回文整数，返回 true ；否则，返回 false 。
 * 回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。例如，121 是回文，而 123 不是。
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
        int len = str.size();
        int beg = 0;
        int end = len - 1;
        for(; beg < end; beg++, end--){
            if(str[beg] != str[end])
            return false;
        }
        return true;   
    }
};
// @lc code=end
//Accepted
// 11510/11510 cases passed (8 ms)
// Your runtime beats 77.91 % of cpp submissions
// Your memory usage beats 56.48 % of cpp submissions (5.8 MB)

