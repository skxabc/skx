import re

print('------------.* match 替换字符串------------')
namesRegex = re.compile(r'Agent \w+')
print(namesRegex.sub("SKX", "Agent ali is a good man"),"\n\n\n\n")
 
print('------------.* match 不区分大小写的匹配-------------')
rebocop = re.compile(r'robotcop',re.I)
print(rebocop.search('RobotcoP is part man').group(),'\n\n\n')

print('------------.* match 换行符-------------')
newlineRegex = re.compile('.*', re.DOTALL)
mo = newlineRegex.search('serve the public trust.\nProtect the innocent\nuphold the law')
print(mo.group())
print('------------.-------------')
atRegex = re.compile(r'the cat (.*) hat (.*)')
mo=atRegex.search('the cat in the hat sat on the flat mat')
print(mo.group())
print(mo.group(1))
print(mo.group(2))

# print("-------------------^------------------")
beginsRegex = re.compile(r'^\d+$')
mo = beginsRegex.search('3s34348')
print(mo.group())
print(mo.group(0))
print(mo.group(1))


print("--------------------do not use regex-----------------------------")
#check a phone number is valid or not,mode like this:415-555-4242
def isPhoneNumer(text):
    if len(text) != 12:
        return False
    for i in range(0,3):
        if not text[i].isdecimal():
            return False
    if text[3] != '-':
        return False
    for i in range(4,7):
        if not text[i].isdecimal():
            return False
    if text[7] != '-':
        return False
    for i in range(8,12):
        if not text[i].isdecimal():
            return False
    return True
'''print('415-222-4343 is a phone number:')
print(isPhoneNumer('415-222-4343'))
print('Moshi is a phone number:')
print(isPhoneNumer("Moshi"))'''
message = 'Call me at 415-222-3232 tomorrow. 415-222-9999 is my office'
for i in range(len(message)):
    chunk = message[i:i+12]
    if isPhoneNumer(chunk):
        print('Phone number found: ' + chunk)
print('Done')



print("--------------------use regex-----------------------------")
phoneNumberRegex = re.compile(r'(\(\d{3}\))?-(\d{3})-(\d{4})')
mo = phoneNumberRegex.search('My number is (415)-333-4343')
print(mo.group(0))
print (mo.group(1))
print(mo.group(2))
print(mo.group(3))
print(mo.groups())
first,second,third=mo.groups()
print(first)
print(second)
print(third)

print("----------------char symbol classification--------------")
xmasRegex = re.compile(r'\d+\s\w+')
print(xmasRegex.findall("12 durm, 11 pie, 10d, 9 shi, 8 hao"))

vovRegex = re.compile(r'[^aeiouAEIOU]')
print(vovRegex.findall("robo cope matlab baby"))

print("-------------------findall---------------")
phoneNumberRegex = re.compile(r'-(\d\d\d)-(\d\d\d\d)')
mo = phoneNumberRegex.search('cell:455-455-4343 work: 212-313-2323')
print(mo.group())

print(phoneNumberRegex.findall('cell:455-455-4343 work: 212-313-2323'))


mo1 = phoneNumberRegex.search('her number is -333-4343')
print("mo1.group(0):",mo1.group(0))
print("mo1.group(1):",mo1.group(1))
print("mo1.group(2):",mo1.group(2))


print("--------------------group +-----------------------------")
batRex = re.compile(r'Bat(wo)+man')
mo = batRex.search("The Adventures of Batman")

mo1 = batRex.search("Thea Adventures of Batwoman")
print(mo1.group())

mo2 = batRex.search("the adventures of Batwowowowowowowoman")
print(mo2.group())

print("--------------------\d-----------------------------")
phoneNumRegex = re.compile(r'\d\d\d-\d\d\d-\d\d\d\d')
mo = phoneNumRegex.search('My number is 415-222-3232')
print('Phone number found: '+ mo.group())



print("--------------------pipeline-----------------------------")
strRegex = re.compile(r'shikaixun|haoyue')
mo = strRegex.search("shikaixun and haoyue is couple")
print("mo", mo.group())
mo1 = strRegex.search("haoyue and shikaixun is couple")
print("mo1:", mo1.group())

batRegex = re.compile(r'bat(man|fill|water|son)')
mo = batRegex.search("batfill is animal")
print(mo.group())
print("group(1)",mo.group(1))
print("groups():",mo.groups())


print("----------------------group?---------------------------")
batRegex = re.compile(r'Bat(wo)?man')
mo = batRegex.search('The Adventures of Batman')
print("mo.group:", mo.group())

mo1 = batRegex.search('The Adventures of Batwoman')
print("mo.group:", mo1.group())