'''
Created on Feb 11, 2018

@author: rabihkodeih
'''

def parseParenthesis(S):    
    left = 0
    right = 0
    result = 0
    for i in range(len(S)):
        if S[i] == ')': 
            right += 1
    for i in range(len(S)):
        if S[i] == '(': 
            left += 1
        else:
            right -= 1
        if left == right:
            result = i + 1
            break
    return result

if __name__ == '__main__':
    S = '(((())(('
    res = parseParenthesis(S)
    print(res)        
    
# Backend: 
#TODO: comments, 
#TODO: functions and variables were cleanly named

# Frontend: component framework Element.io, UX made sense to the user
# Tests: API full frontend E2E tests, CI platform such as TravisCI or CircleCI to the repo
# Deployment: zappa, Cloud Formation scripts
# Documentation: how to deploy the app, screenshots of rendered UI, ERDs, workflows, etc

# My scores:
#     Requiremtns    5
#     Backend        5
#     Frontend       5
#     Tests          0
#     Deployment     9
#     Docs           8 




#TODO: make sure that in all files, we have imports are properly formatted








