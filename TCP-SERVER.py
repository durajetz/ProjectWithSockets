import socket
import sys
import datetime
import random
from _thread import *


host = 'localhost'
port = 13000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("FIEK TCP SERVER")

try:
    serverSocket.bind((host, port))
except socket.error:
    print("Startimi i serverit deshtoi! Binding Failed.")
    sys.exit()
print("""================================================================
Serveri ka startuar ne hostin """+"|"+host+"|" +" me port |"+str(port)+"|")


serverSocket.listen(5)
print("Serveri eshte i gatshem te pranoje kerkesa...\n================================================================")

def ipaddr(adresa):
    return adresa[0]

def portnr(adresa):
    return adresa[1]

def count(fjalia):
    string2=fjalia.upper()                              
    k=0        
    n=0                                           
    for char in string2:                                   
        if char in 'AEIOUY':                               
            k += 1
        elif (char.isalpha()) == True:
            n += 1
        # else:  #Ne raste se deshirojm qe inputi te permbaj vetem karaktere te alfabetit                         
        #     return str("GABIM,ju duhet te jepni nje varg te karakterve(String)")                                        
    return str("\" " + fjalia+"\""+" ka " + str(k) + " zanore dhe " + str(n) + " bashketingellore") 

def reverse(fjalia):
    return fjalia[::-1].strip() # mos me lon hapsira ne fillim dhe fund

def palindrome(fjala):
    string1 = fjala.replace(" ","")  #Ne rast se e shkruajm psh: mad[hapsir]am --> me na e shfaq true
    if(string1[::1]==string1[::-1]):
      return True
    else:
      return False    

def time():
    now = datetime.datetime.now()
    return "Data dhe koha tani: " + now.strftime("%d.%m.%Y , %I:%M:%S %p")


def game():
    answer = set()
    i = 0
    while i < 5:
        r = random.randint(1,35)
        if r not in answer:
            i += 1
            answer.add(r)
    return str(sorted(answer)).replace('[', '(').replace(']', ')')


def konverto(opsioni, vlera):
    if opsioni=="cmToFeet":
        rezultati=vlera / 30.4

    elif opsioni=="FeetToCm":
        rezultati=vlera * 30.4 

    elif opsioni=="kmToMiles":
        rezultati = vlera / 1.6

    elif opsioni=="MileToKm":
        rezultati = vlera * 1.6
    else:
        rezultati="Zgjedhni njeren nga opcionet"
    return str(round(rezultati, 2))

def gcd(nr1,nr2):
    while nr2 != 0:
        (nr1, nr2) = (nr2, nr1 % nr2)
    return nr1

#METODA EXTRA
MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                   'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.',
                   'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ',': '--..--', '.': '.-.-.-',
                   '?': '..--..', '/': '-..-.', '-': '-....-',
                   '(': '-.--.', ')': '-.--.-'}


def MorseCode(opsioni,message):
    if(opsioni == "ENCODE"):
        cipher = ''
        for letter in message.upper():
            if letter != ' ':
                cipher += MORSE_CODE_DICT[letter] + ' '
            else:
                cipher += ' '
        return "Cipher Teksti: " + cipher
    elif(opsioni == "DECODE"):
        message += ' '  
        decipher = ''
        citext = ''
        for letter in message.upper():
            if(letter != ' '):
                i = 0  
                citext += letter  
            else:
                i += 1
                if i == 2:
                    decipher += ' '
                else:
                    decipher += list(MORSE_CODE_DICT.keys()
                                 )[list(MORSE_CODE_DICT.values()).index(citext)]
                    citext = ''
        return "Plain Teksti: " + decipher
    else:
        return "Zgjedhni njeren nga opcionet"



 

def client_thread(conn,address):
    try:
        while True:
            methodByte = conn.recv(128)
            method = methodByte.decode("utf-8")

            select=str(method).split(" ")
            teksti = ""
            i = len(select)
            for fjala in range (1,i):
                teksti += select[fjala]
                if(fjala!=i):
                    teksti +=" "

            if not method:
                break
            if  (select[0]=="IPADDRESS"):
                answer = "IP adresa e Klientit eshte: " + ipaddr(address)
            elif (select[0]=="PORT"):
                answer = "Klienti eshte duke perdorur portin " + str(portnr(address))
            elif (select[0]=="COUNT"):
                if not teksti.strip():
                    answer = "Shkruani ndonje fjal apo fjali!"
                else:
                    answer = (count(teksti))
            elif(select[0]=="REVERSE"):                                                      
                if not teksti.strip():
                    answer="Shkruani ndonje fjal apo fjali!"
                else:
                    answer="Fjalia e kthyer mbrapsht:"+reverse(teksti)                
            elif(select[0]=="PALINDROME"):
                if not teksti.strip():
                    answer="Shkruani ndonje fjal apo fjali!"
                else:
                    answer=str(palindrome(teksti))
            elif (select[0]=="TIME"):
                    answer = time()
            elif (select[0]=="GAME"):
                    answer = game()
            elif(select[0]=="CONVERT"):
                try:
                    numri=float(select[2]) 
                    answer="Vlera e konvertuar eshte: "+str(konverto(select[1], numri))               
                except Exception:
                    answer="Argument jo valid!"
            elif(select[0]=="GCF"):
                try:
                    numri1=int(select[1])
                    numri2=int(select[2])
                    answer="Faktori me i madh i perbashket eshte: "+str(gcd(numri1,numri2))
                except Exception:
                    answer="Argument jo valid!"
            elif(method.startswith("MORSE-CODE")):
                try:
                    if not teksti.strip():
                        answer="Per enkodim shkruani"
                    else:
                        answer=str(MorseCode(select[1],method[18:]))
                except Exception:
                    answer="Argument jo valid!"                
            else:
                answer = "Keni dhene nje komande jo valide!"
                print("Klienti ka dhene komande jo valide!")
            conn.sendall(str.encode(answer))
            print("Klientit " + "|" + address[0]+ "|" + " iu dergua pergjigja: " + "/" + str(answer) + "/")
        conn.close()
    except ConnectionResetError:
        print("================================================================\nKlienti humbi lidhjen me server!\n================================================================")
    except ConnectionAbortedError: 
        print("================================================================\nKlienti humbi lidhjen me server!\n================================================================")


while True:
    connection, address = serverSocket.accept()
    print("""Serveri u lidh me klientin """ + address[0] + " me port "+ str(address[1]) +"\n"
    "================================================================")
    start_new_thread(client_thread, (connection,address,))

serverSocket.close()
