from KeyGenerator import KeyGenerator
from shahash import shasaltpass
class EncDec:
    def __init__(self,bits=3000):
        self.__kg=KeyGenerator(bits)
        self.__sha=shasaltpass(40,20,"ASCII")
    def __str2int(self,st):
        s=0
        for i in range(len(st)):
            s+=256**i*ord(st[-(i+1)])
        return s
    def __int2str(self,s):
        st=""
        while s>0:
            te=s%256
            st=chr(te)+st
            s//=256
        return st
    def encrypt(self,mes):
        return self.__int2str(pow(self.__str2int(self.__sha.hashRegister(mes)),self.__kg.e,self.__kg.n))
    def check(self,mes,encrypted_mes):
        emes=self.__int2str(pow(self.__str2int(encrypted_mes),self.__kg.d,self.__kg.n))
        return self.__sha.hashVerify(mes,emes)