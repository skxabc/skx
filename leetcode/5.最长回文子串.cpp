/*
 * @lc app=leetcode.cn id=5 lang=cpp
 *
 * [5] 最长回文子串
 */

// @lc code=start
#include<iostream>
#include<string>
using namespace std;

//abcbd
// string Palindrome(string s1, int l, int r){
//     while(l>=0 && r < s1.length() && s1[l] == s1[r]){
//         l--;
//         r++;
//     };

//     return s1.substr(l+1, r-l-1);
// }
// class Solution {
// public:
//     string longestPalindrome(string s) {
//         int len = s.length();
//         string tmp = "";
//         if(len == 1)return s;
//         for(int i = 0; i < len; i++){
//             string s1 = Palindrome(s, i, i);
//             string s2 = Palindrome(s, i, i+1);
//             tmp = tmp.length()>s1.length()?tmp:s1;
//             tmp = tmp.length()>s2.length()?tmp:s2;
//         }
//         return tmp;
//     }
// };
// @lc code=end
//Accepted
//141/141 cases passed (72 ms)
//Your runtime beats 55.39 % of cpp submissions
//Your memory usage beats 29.42 % of cpp submissions (164.6 MB)
//上述中心扩散法，缺点是里面有很多重复计算，动态规划就是解决重复计算问题，空间换时间。



string Palindrome(string s1, int l, int r){
    while(l>=0 && r < s1.length() && s1[l] == s1[r]){
        l--;
        r++;
    };

    return s1.substr(l+1, r-l-1);
}
class Solution {
public:
    string longestPalindrome(string s) {
        int len = s.length();
        string tmp = "";
        if(len == 1)return s;
        for(int i = 0; i < len; i++){
            string s1 = Palindrome(s, i, i);
            string s2 = Palindrome(s, i, i+1);
            tmp = tmp.length()>s1.length()?tmp:s1;
            tmp = tmp.length()>s2.length()?tmp:s2;
        }
        return tmp;
    }
};