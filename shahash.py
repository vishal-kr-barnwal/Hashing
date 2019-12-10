class shasaltpass:
    import numpy as __np
    def __init__(self,MaxCharCount,MinSaltCharCount,OperatingFormat="ASCII",RotationOffsetMatrix="Optional"):
        try:
            if(OperatingFormat.upper()=="ASCII"):
                self.n=8
            elif(OperatingFormat.upper()=="UNICODE"):
                self.n=16
            else:
                raise Exception("Operating Format must be in either ASCII or UNICODE")
            if (type(MaxCharCount)!=int or MaxCharCount<8 or MaxCharCount>(1024/self.n)):
                raise Exception("Character Count Should be int and belongs to [8,"+str(1024//self.n)+"]")
            else:
                self.ml=MaxCharCount
                self.pl=MaxCharCount+MinSaltCharCount
            if MinSaltCharCount>(576//self.n):
                raise Exception("Minimum Salting Character Count should be less than "+str(576//self.n))
            if(RotationOffsetMatrix=="Optional"):
                self.__ro=[[0,36,3,41,18],\
                           [1,44,10,45,2],\
                           [62,6,43,15,61],\
                           [28,55,25,21,56],\
                           [27,20,39,8,14]]
            else:
                try:
                    a=(len(RotationOffsetMatrix)!=5)
                    for i in range(5):
                        a=(a or len(RotationOffsetMatrix[i])!=5)
                    if a:
                        raise Exception("Enter Rotation Offset Matrix as int matrix of dimension 5\u00D75"+\
                                       "and should belong to [0,64)")
                    self.__ro=[[0]*5]*5
                    for i in range(5):
                        for j in range(5):
                            tem=RotationOffsetMatrix[i][j]
                            if(type(tem)!=int or tem<0 or tem>63):
                                raise Exception("Enter Rotation Offset Matrix as int matrix of dimension 5\u00D75"+\
                                               "and should belong to [0,64)")
                            self.__ro[i][j]=tem
                except:
                    raise Exception("Enter Rotation Offset Matrix as int matrix of dimension 5\u00D75"+\
                                   "and should belong to [0,64)")
        except:
            raise Exception("Arguments should by of datatype [integer,string,(optional) 4-bit integer 5\u00D75 matrix]")
    def __one2three(self,a):
        b=self.__np.zeros((5,5,64),dtype=bool)
        for i in range(5):
            for j in range(5):
                for k in range(64):
                    b[i,j,k]=a[64*(5*j+i)+k]
        return b
    def __three2one(self,a):
        b=self.__np.zeros(1600,dtype=bool)
        for i in range(5):
            for j in range(5):
                for k in range(64):
                    b[64*(5*j+i)+k]=a[i,j,k]
        return b
    def __str2bin(self,st):
        a=[]
        for i in st:
            temb=bin(ord(i))[2:]
            a+=[0]*(self.n-len(temb))
            for j in temb:
                a+=[ord(j)-48]
        return self.__np.array(a,dtype=bool)
    def __bin2str(self,bi):
        bi=self.__np.array(bi,dtype=int)
        s=''
        for i in range(len(bi)//self.n):
            tems=''
            for j in range(i*self.n,(i+1)*self.n):
                tems+=str(bi[j])
            s+=chr(int(tems,2))
        return s
    def __saltGen(self,st):
        ma=2**self.n
        salt=""
        for i in range(self.pl-len(st)):
            salt+=chr(self.__np.random.randint(ma))
        return salt
    def __saltIn(self,st,salt):
        return (salt[:len(salt)//2]+st+salt[len(salt)//2:])
    def __theta(self,a):
        b=self.__np.zeros((5,5,64),dtype=bool)
        for i in range(5):
            for j in range(5):
                for k in range(64):
                    l=(i+1)%5
                    b[i,j,k]=a[i,j,k]^((a[l,4,k-1]^((a[l,0,k-1]^a[l,1,k-1])^\
                                                    (a[l,2,k-1]^a[l,3,k-1])))\
                                       ^(a[i-1,4,k]^((a[i-1,0,k]^a[i-1,1,k])\
                                                     ^(a[i-1,2,k]^a[i-1,3,k]))))
        return b
    def __rho(self,a):
        b=self.__np.zeros((5,5,64),dtype=bool)
        for i in range(5):
            for j in range(5):
                for k in range(64):
                    b[i,j,k]=a[i,j,k-self.__ro[i][j]]
        return b
    def __pi(self,a):
        b=self.__np.zeros((5,5,64),dtype=bool)
        for i in range(5):
            for j in range(5):
                for k in range(64):
                    b[i,j,k]=a[i,(2*i+3*j)%5,k]
        return b
    def __chi(self,a):
        b=self.__np.zeros((5,5,64),dtype=bool)
        for i in range(5):
            for j in range(5):
                for k in range(64):
                    b[i,j,k]=a[i-3,j,k]&(a[i-4,j,k]^a[i,j,k])
        return b
    def __lffsr(self,a):
        return self.__np.append(a[1:],(a[-1]^a[-1])^(a[-3]^a[0]))
    def __iota(self,a,rd):
        b=a
        bit=self.__np.zeros(64,dtype=bool)
        rc=self.__np.zeros(168,dtype=bool)
        w=self.__np.array([1]+[0]*6,dtype=bool)
        rc[0]=w[0]
        for i in range(1,168):
            w=self.__lffsr(w)
            rc[i]=w[0]
        for i in range(7):
            bit[2**i-1]=rc[i+7*rd]
        for k in range(64):
            b[0,0,k]=a[0,0,k]^bit[k]
        return b
    def __prepare(self,bi):
        return self.__np.array(bi.tolist()+(self.__np.array([0]*(1600-len(bi)),dtype=bool)).tolist(),dtype=bool)
    def __hashOut(self,st,salt):
        st=self.__saltIn(st,salt)
        bi=self.__str2bin(st)
        bi=self.__one2three(self.__prepare(bi))
        for i in range(24):
            bi=self.__iota(self.__chi(self.__pi(self.__rho(self.__theta(bi)))),i)
        return (salt[len(salt)//2:]+self.__bin2str(self.__three2one(bi))+salt[:len(salt)//2])
    def hashRegister(self,st):
        if len(st)<8 or len(st)>self.ml:
            raise Exception('Password should be of minimum 8 charcters and maximum '+str(self.ml)+' character')
        return self.__hashOut(st,self.__saltGen(st))
    def __saltExtract(self,ha):
        sl=len(ha)-1600//self.n
        return (ha[(len(ha)-sl//2):]+ha[:(sl-sl//2)])
    def hashVerify(self,st,ha):
        return (ha==self.__hashOut(st,self.__saltExtract(ha)))