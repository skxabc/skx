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
