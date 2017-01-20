import unicodedata

def decode(input): 
        output = input.encode('utf-8', 'strict').decode('utf-8');
        return ''.join(map(uord, output))
    
def uord(x): 
        num = ord(x)
        if num < 128:
            return x
        else:
            return '\\u' + str(num) + ' '


