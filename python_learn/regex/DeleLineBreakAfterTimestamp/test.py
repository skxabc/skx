import re
f=open("./test.txt", 'r+')
f1=open("./test.txt.bak", 'w')
for line in f:
    #out=re.sub(r'(?<=[0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3})\n',"", line)
    out=re.sub(r'(?<=\d\d\d)\s',"", line)
    print(out)
    f1.write(out)