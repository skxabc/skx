/*
 * @lc app=leetcode.cn id=1 lang=cpp
 *
 * [1] 两数之和
 */

// @lc code=start
// class Solution {
// public:
//     vector<int> twoSum(vector<int>& nums, int target) {
//         vector<int> arrRet;
//         int len = nums.size();
//         for(int i = 0; i < len; ++i)
//         {
//             for (int j = i+1; j < len; ++j)
//             {
//                 if(target == nums[i] + nums[j])
//                 {
//                     arrRet.push_back(i);
//                     arrRet.push_back(j);
//                 }
//             }
//         }
//         return arrRet;
//     }
// };
/*上述方法性能
53/53 cases passed (60 ms)
Your runtime beats 5.62 % of cpp submissions
Your memory usage beats 69.26 % of cpp submissions (8.7 MB)*/
// class Solution {
// public:
//     vector<int> twoSum(vector<int>& nums, int target) {
//         map<int,int>a;
//         vector<int>b(2,-1);
//         for(int i = 0; i < nums.size(); ++i)
//         {
//             a.insert(map<int,int>::value_type(nums[i],i));
//         }
        
//         for (int i = 0 ; i < nums.size(); ++i)
//         {
//             if(a.count(target - nums[i]) > 0 && a[target - nums[i]] != i)
//             {
//                 b[0] = i;
//                 b[1] = a[target - nums[i]];
//                 break;
//             }
//         }
//         return b;
//     };
// };

/*
Accepted
53/53 cases passed (8 ms)
Your runtime beats 72.56 % of cpp submissions
Your memory usage beats 12.04 % of cpp submissions (9.9 MB)*/

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        map<int,int>mapEleIdx;
        vector<int>vecRet(2,-1);
        for(int i = 0; i < nums.size(); ++i)
        {
            if(mapEleIdx.count(target - nums[i]) > 0)
            {
                vecRet[1] = i;
                vecRet[0] = mapEleIdx[target - nums[i]];
            }
            else
            {
                //mapEleIdx[nums[i]] = i;
                mapEleIdx.insert(std::pair<int,int>(nums[i],i));
            }
            
        }
        return vecRet;    
    };
};
/*53/53 cases passed (12 ms)
Your runtime beats 42.85 % of cpp submissions
Your memory usage beats 7.93 % of cpp submissions (10.1 MB)*/
// @lc code=end
