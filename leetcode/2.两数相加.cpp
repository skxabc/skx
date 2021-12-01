// @before-stub-for-debug-begin
#include <vector>
#include <string>
#include "commoncppproblem2.h"

using namespace std;
// @before-stub-for-debug-end

/*
 * @lc app=leetcode.cn id=2 lang=cpp
 *
 * [2] 两数相加
 */

// @lc code=start
/**
  Definition for singly-linked list.*/
//   struct ListNode {
//       int val;
//       ListNode *next;
//       ListNode() : val(0), next(nullptr) {}
//       ListNode(int x) : val(x), next(nullptr) {}
//       ListNode(int x, ListNode *next) : val(x), next(next) {}
//   };

class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        if(nullptr == l1) return l2;
        if(nullptr == l2) return l1;
        
        ListNode *l3 = new ListNode(0);
        // ListNode l3();
        ListNode *head = l3;
        if(l1->next == nullptr && l2->next == nullptr){
            l2->val = l2->val + l1->val;
            if(l2->val >= 10){
                l3->val = (l2->val)%10;
                l3->next = new ListNode(1);
                return head;
            }
            return l2;
        }
        int flag = 0;
        int l1len = 0;
        int l2len = 0;
        ListNode* tmp1 = l1;
        ListNode* tmp2 = l2;
        while(tmp1 != nullptr){
            l1len++;
            tmp1 = tmp1->next;
        }
        while(tmp2 != nullptr){
            l2len++;
            tmp2 = tmp2->next;
        }
        cout<<"l1 len:"<<l1len<<" l2 len:"<<l2len<<endl;
        if(l1len == l2len){
            while(l1 != nullptr){
                if(flag == 1){
                    l3->val = l1->val + l2->val + 1;
                    flag = 0;
                }else{
                    l3->val = l1->val + l2->val;
                }

                if(l3->val >= 10){
                    flag = 1;
                    l3->val = (l3->val)%10;
                }
                l1 = l1->next;
                l2 = l2->next;
                if(nullptr != l1){
                    l3->next = new ListNode(0);
                    l3 = l3->next;
                }
                cout<<"l3: "<<l3->val<<endl;
            }
            
        }else if(l1len < l2len){
            while(l2 != nullptr){
                if(flag == 1){
                    if(l1 != nullptr){
                        l3->val = l1->val + l2->val + 1;
                        l1 = l1->next;
                    }else{
                        l3->val = l2->val + 1;
                    }
                    flag = 0;
                    
                }else{
                    if(l1 != nullptr){
                        l3->val = l1->val + l2->val;
                        l1 = l1->next;
                    }else{
                        l3->val = l2->val;
                    }
                }
                if(l3->val >= 10){
                    flag = 1;
                    l3->val = (l3->val)%10;
                }
                cout<<"l3: "<<l3->val<<endl;
                l2 = l2->next;
                if(nullptr != l2){
                    l3->next = new ListNode(0);
                    l3 = l3->next;
                }
                
            }
        }else if(l1len > l2len){
            cout<<"l1len > l2len"<<endl;
            while(l1 != nullptr){
                cout<<"l1 != nullptr"<<endl;
                if(flag == 1){
                    if(l2 != nullptr){
                        l3->val = l2->val + l1->val + 1;
                        l2 = l2->next;
                    }else{
                        l3->val = l1->val + 1;
                    }
                    flag = 0;
                    cout<<"l3 1:"<<l3->val<<endl;
                }else{
                    if(l2 != nullptr){
                        l3->val = l1->val + l2->val;
                        l2 = l2->next;
                    }else{
                        l3->val = l1->val;
                    }
                    cout<<"l3 2:"<<l3->val<<endl;
                }
                if(l3->val >= 10){
                    flag = 1;
                    l3->val = (l3->val)%10;
                }
                cout<<"l3 3:"<<l3->val<<endl;
                l1 = l1->next;
                if(nullptr != l1){
                    l3->next = new ListNode(0);
                    l3 = l3->next;
                }
                
            }
        }
        if(flag == 1){
            l3->next = new ListNode(0);
            l3 = l3->next;
            l3->val = 1;
            l3->next = nullptr;
        }else{

        }
        return head;
    }
};
// @lc code=end

