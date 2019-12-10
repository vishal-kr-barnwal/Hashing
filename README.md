# Hashing
Dual layer hashing (random salted SHA3 1600 bits &amp; 2048 bit RSA for security improvisation).
# Programming Language - Python3
<I>Libraries needed : </I> Numpy
# Prime Generator
Program to get next prime number efficiently and fastly for getting RSA keys. 
<br>File containing progran is primegenerator.py. Here, function defined for getting next prime is next_prime.
# Key Generator
File is KeyGenerator.py.
<br>It has a class KeyGenerator containing all the three keys required for RSA encryption.
<br>On initialization with Number Of Bits it gives us unique keys for RSA encryption. 
<br>It contains 3 variables 'e' and, 'n' as public key. And, 'd' as private key. 
# SHA Hashing
File is shasaltpass.py.
<br>It has a class shasaltpass which contains the whole program. 
<br>It has two functions :
<br><I><B>hashRegister : </B>This encrypt string using random salts and returns hash embedded with salt.</I>
<br><I><B>hashVerify : </B>It has two inputs string to be compared and hash. It extract salt from hash and using that hash generate hash. It return boolean value for whether generated hash and input hash are same or not.</I>
# Securing hash
Algorithm used is RSA. 
<br>It is done in order to secure the hash so that salt can't be easily extracted. Thus, giving user dual security as their own password and system generated unique password. 
<br>It has two functions :
<br><I><B>encrypt : </B>This generate salt embedded hash using SHA3 and then, using RSA it further encrypt the hash in order to hide salt. This gives us a new hash which is dually encrypted. </I>
<br><I><B>check : </B>This decrypt encrypted hash and then use hashVerify method of shasaltpass to verify the password entered. </I>
# Main
Loads EncDec class which contains final encrypt and check function.
