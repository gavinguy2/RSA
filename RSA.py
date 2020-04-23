import random
import math
from math import gcd as bltin_gcd

class RSA:

    def GenerateKeys(self,sP,sQ):
        P = self.twentySixToTen(sP) % pow(10,200)
        Q = self.twentySixToTen(sQ) % pow(10,200)
        if P % 2 == 0:
            P += 1
        if Q % 2 == 0:
            Q += 1
        while not self.isPrimeMiller(P):
            P += 1
        while not self.isPrimeMiller(Q):
            Q += 1
        N = P * Q
        R = (P - 1)*(Q - 1)
        E = R % pow(10,398)
        if E % 2 == 0:
            E += 1
        while not self.coprime(E,R):
            E += 1
        D = self.modinv(E,R)
        f = open("public.txt","w")
        f.write(str(N))
        f.write("\n")
        f.write(str(E))
        f.close()
        f = open("private.txt","w")
        f.write(str(N))
        f.write("\n")
        f.write(str(D))
        f.close()
        print("Keys Generated")
        
# Everything Generate Keys uses###########################################    
    def egcd(self,a,b):
        x,y, u,v = 0,1, 1,0
        while a != 0:
            q, r = b//a, b%a
            m, n = x-u*q, y-v*q
            b,a, x,y, u,v = a,r, u,v, m,n
        gcd = b
        return gcd, x, y
    
    def coprime(self,a, b):
        return bltin_gcd(a, b) == 1
    
    def modinv(self,a,m):
        gcd, x, y = self.egcd(a, m)
        if gcd != 1:
            return None
        else:
            return x % m
        
    def MillersTest(self,n,b):
        t = n-1
        s = 0

        while t % 2 == 0:
            s+=1
            t //=2
        t = int(t)
        b = int(b)
        n = int(n)
        if pow(b,t,n) == 1:
            return True
   
        for i in range(s):
            if pow(b,t,n) == n-1:
                return True
            t*=2
        
        return False
        
    def isPrimeMiller(self,n):
        for i in range(1):
            b = random.randrange(2,n-1)
            millerpass = self.MillersTest(n,b)
            if not millerpass:
                return False
        return True

    def twentySixToTen(self,num):
        base_twentysix = "abcdefghijklmnopqrstuvwxyz"
        bten = 0
        for c in num:
            if c in base_twentysix:
                bten = bten*26
                bten += base_twentysix.index(c)
            else:
                print ("Invalid character in string: ",c)
                return 0
        return bten
# End of Generate Keys functions. To 70 base changed ##########################################

    def seventyToTen(self,string):
        base_seventy = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.?! \t\n\r"
        value = 0
        for c in string:
            index = base_seventy.find(str(c))
            if index !=-1:
                value *= len(base_seventy)
                value += index
        return value
        
        
    def tenToSeventy(self,bten):
        base_seventy = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.?! \t\n\r"
        bseventy = ""
        charlist = []
        num = bten
        while num > 0:
            remainder = num%70
            
            num = num//70
            charlist.append(base_seventy[int(remainder)])
        for i in range(len(charlist)-1,-1,-1):
            bseventy += charlist[i]
        return bseventy
    
##############################################################################################
    
    def Encrypt(self,inputfile):
        print ("Encrypting")
        fin = open(inputfile,"rb")
        PlainTextBinary = fin.read()
        PlainText = PlainTextBinary.decode("utf-8")
        fin.close()
        pt = open("public.txt","r")
        N = int(pt.readline())
        E = int(pt.readline())
        pt.close()
        new = ""
        bz = int(math.log(N,70))
        fout = open("outputfile.txt","wb")
        l = []
        for i in range(0,len(PlainText), bz):
            l.append(PlainText[i:i+bz])
        for b in l:
            if b == "":
                break
            f = self.seventyToTen(b)
            ff = pow(f,E,N)
            fout.write(self.tenToSeventy(ff).encode("utf-8"))
            fout.write("$".encode("utf-8"))
        fout.close()
        g = open("private.txt","r")
        N = int(g.readline())
        D = int(g.readline())
        
#############################################################################################
        
    def Decrypt(self,encFile):
        fin = open(encFile,"rb")
        blocks = fin.read().decode("utf-8")
        blocks = blocks.split("$")
        fin.close()
        g = open("private.txt","r")
        N = int(g.readline())
        D = int(g.readline())
        g.close()
        h = open("decrypt.txt","wb")
        for b in blocks:
            if b == "":
                break
            else:
                bb = self.seventyToTen(b)
                
                dec = pow(bb,D,N)
                h.write(self.tenToSeventy(dec).encode("utf-8"))
        h.close()
        print ("Decryption complete.")
        
#############################################################################################
        
def main():
    r = RSA()
    r.GenerateKeys("fvjknfwwefnwefwcfkwefnfwqwertyhgfgdhjdnbfghdjdnfbgryuejdnfbhjdffwcfkwefnfwqwertyhgfgdhjdnbfghdjdnfbgryuejdnfbhjdfhdjfhdjbhunhubgyvbhubgyvhdjfhdjbhunhubgyvbhubgyvftcdrxsexdcftvgbhnhubgvfhfehfrihfihfweihfwbgbvhfyfhfehergrejherhgergreihfihrfihfjhfjmmnzheghifwihivejbvefjvfekjvefkkkkdjdjdebfejhnfwcfkwefnfwqwertyhgfgdhjdnbfghdjdnfbgryuejdnfbhjdfhdjfhdjbhunhubgyvbhubgyvihfrfihwifhweiufhiefncnvna","uhirehfirehnjdfowjfoejfowjfowenfoewjfowertyuiknhgfghbvftyhbvffwcfkwefnfwqwertyhgfgdhjdnbfghdjdnfbgryuejdnfbhjdfhdjfhdjbhunhubgyvbhubgyvfwcfkwefnfwqwertyhgfgdhjdnbfghdjdnfbgryuejdnfbhjdfhdjfhdjbhunhubgyvbhubgyvghbghjdnfjdjnfjkdmkmnjfhgfhdjbfghjhfbghjfhbghjfhgbfhjhghhgbhnbhjbhevbhjvvefbhjfvebhjfvehjbqtyjnbvghjbghjmnbghjmnbhjcnjgehifrgregrrgehireirgihgriiuuigreuiheriuhhbnbvfgyhbvghjbvghnbghjbghjuweihfiuwhfiudhiuhfwiuehiuwhf")
    r.Encrypt("input.txt")
    r.Decrypt("outputfile.txt")
main()
