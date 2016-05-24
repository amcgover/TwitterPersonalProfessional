import re
def replaceEmojis(s):
    if type(s) != str:
        raise TypeError('ERROR, either null string or non-string type entered to replaceEmojis function')
    
    s = re.sub(r"[\U0001F600-\U0001F64F]",'<emoji>',s);
    s = re.sub(r"[\U00002702-\U000027B0]",'<emoji>',s);
    s = re.sub(r"[\U0001F680-\U0001F6C0]",'<emoji>',s);
    s = re.sub(r"[\U000024C2-\U0001F251]",'<emoji>',s);
    s = re.sub(r"[\U0001F600-\U0001F636]",'<emoji>',s);
    s = re.sub(r"[\U0001F681-\U0001F6C5]",'<emoji>',s);
    s = re.sub(r"[\U0001F30D-\U0001F567]",'<emoji>',s);
    return s
