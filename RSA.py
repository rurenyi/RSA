import random
from random import randint


def proBin(w): 
    list = []
    list.append('1')
    for _ in range(w - 2):
        c = random.choice(['0', '1'])
        list.append(c)
    list.append('1')
    res = int(''.join(list),2)
    return res

def X_n_mod_P(base, exponent, n):
    bin_array = bin(exponent)[2:][::-1]
    r = len(bin_array)
    base_array = []
    
    pre_base = base
    base_array.append(pre_base)
    
    for _ in range(r - 1):
        next_base = (pre_base * pre_base) % n 
        base_array.append(next_base)
        pre_base = next_base
        
    a_w_b = __multi(base_array, bin_array, n)
    return a_w_b % n

def __multi(array, bin_array, n):
    result = 1
    for index in range(len(array)):
        a = array[index]
        if not int(bin_array[index]):
            continue
        result *= a
        result = result % n
    return result

def MillerRabin(a, p):
    if X_n_mod_P(a, p - 1, p) == 1:
        u = (p-1) >> 1
        while (u & 1) == 0:
            t = X_n_mod_P(a, u, p)
            if t == 1:
                u = u >> 1
            else:
                if t == p - 1:
                    return True
                else:
                    return False
        else:
            t = X_n_mod_P(a, u, p)
            if t == 1 or t == p - 1:
                return True
            else:
                return False
    else:
        return False

def testMillerRabin(p, k):
    while k > 0:
        a = randint(2, p - 1)
        if not MillerRabin(a, p):
            return False
        k = k - 1
    return True

def makeprime(w):          
    while 1:
        d = proBin(w)
        for i in range(50): 
            u = testMillerRabin(d+2*(i), 5)
            if u:
                b = d + 2*(i)
                break
            else:
                continue
        if u:
            return b
        else:
            continue

def str_to_int(b):
    return int.from_bytes(b.encode("utf-8"),"little")

def int_to_str(i):
    return i.to_bytes((i.bit_length() + 7) // 8, 'little').decode()


'''
ax + by = 1
'''
def ext_gcd(a, b):
    if b == 0:
        x1 = 1
        y1 = 0
        x = x1
        y = y1
        r = a
        return r, x, y
    else:
        r, x1, y1 = ext_gcd(b, a % b)
        x = y1
        y = x1 - a // b * y1
        return r, x, y

'''
(base ^ exponent) mod n
'''
def exp_mode(base, exponent, n):
    bin_array = bin(exponent)[2:][::-1]
    r = len(bin_array)
    base_array = []
    
    pre_base = base
    base_array.append(pre_base)
    
    for _ in range(r - 1):
        next_base = (pre_base * pre_base) % n 
        base_array.append(next_base)
        pre_base = next_base
        
    a_w_b = __multi(base_array, bin_array, n)
    return a_w_b % n

def __multi(array, bin_array, n):
    result = 1
    for index in range(len(array)):
        a = array[index]
        if not int(bin_array[index]):
            continue
        result *= a
        result = result % n
    return result

def gen_key(p, q):
    n = p * q
    fy = (p - 1) * (q - 1)      
    e = 65537                 
    a = e
    b = fy
    x = ext_gcd(a, b)[1]

    if x < 0:
        d = x + fy
    else:
        d = x
    print("public key:"+"("+str(n)+","+str(e)+")\nself key:"+"("+str(n)+","+str(d)+")")
    return    (n, e), (n, d)


def encrypt(m, pubkey): # m is meaasge
    n = pubkey[0]
    e = pubkey[1]
    
    c = exp_mode(m, e, n)
    return c

def decrypt(c, selfkey):
    n = selfkey[0]
    d = selfkey[1]
    
    m = exp_mode(c, d, n)
    return m
    
    
if __name__ == "__main__":
    print( "generate a prime number larger than 64 bit")
    p = makeprime(528) 
    print("p:",p)
    q = makeprime(528)
    print("q:",q)

    print("generate public key and self key")
    pubkey, selfkey = gen_key(p, q)

    print("input your message here")
    plaintext = str(input())
    m = str_to_int(plaintext)

    print("result of encryption")
    c = encrypt(m, pubkey)
    print(c)
 
    print("result of decrypt")
    d = decrypt(c, selfkey)
    print(int_to_str(d))