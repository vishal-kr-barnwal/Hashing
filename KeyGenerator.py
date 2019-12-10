import random as rand
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
class KeyGenerator:
    def __init__(self,n):
        import primegenerator as pg
        pbit=rand.randint(2**(n//2),2**(2*n//3))
        qbit=rand.randint(2**(n//2),2**(2*n//3))
        p=pg.next_prime(pbit)
        q=pg.next_prime(qbit)
        self.e=pg.next_prime(rand.randint(30,max([2**(n//100),50])))
        self.n=p*q
        phi=(p-1)*(q-1)
        self.d=modinv(self.e,phi)
        del pg,pbit,qbit,p,q,phi