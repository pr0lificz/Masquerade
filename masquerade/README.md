'''text
ggg, ,ggg,_,ggg,                                                                                                     
dP""Y8dP""Y88P""Y8b                                                                                        8I          
Yb, `88'  `88'  `88                                                                                        8I          
 `"  88    88    88                                                                                        8I          
     88    88    88                                                                                        8I          
     88    88    88    ,gggg,gg    ,g,       ,gggg,gg  gg      gg   ,ggg,    ,gggggg,    ,gggg,gg    ,gggg,8I   ,ggg,  
     88    88    88   dP"  "Y8I   ,8'8,     dP"  "Y8I  I8      8I  i8" "8i   dP""""8I   dP"  "Y8I   dP"  "Y8I  i8" "8i 
     88    88    88  i8'    ,8I  ,8'  Yb   i8'    ,8I  I8,    ,8I  I8, ,8I  ,8'    8I  i8'    ,8I  i8'    ,8I  I8, ,8I 
     88    88    Y8,,d8,   ,d8b,,8'_   8) ,d8,   ,d8b ,d8b,  ,d8b, `YbadP' ,dP     Y8,,d8,   ,d8b,,d8,   ,d8b, `YbadP' 
     88    88    `Y8P"Y8888P"`Y8P' "YY8P8PP"Y8888P"88d8P'"Y88P"`Y8888P"Y8888P      `Y8P"Y8888P"`Y8P"Y8888P"`Y8888P"Y888
                                                   I8P                                                                 
                                                   I8'                                                                 
                                                   I8                                                                  
                                                   I8                                                                  
                                                   I8                                                                   '''                                                          I8


Made by *pr0lificz*

Masquerade is a JWT, Token Multi-Tool capable of decoding, cracking and forging JWT Tokens.
Usage: python3 masquerade.py <action> [options]
  Actions: 
  decode:  Decode JWT header and payload 
  Example: python3 masquerade.py decode -t <token>
  
  crack: Brute-force the HMAC secret key using a wordlist
  Example: python3 masquerade.py crack -t <token> -w wordlist.txt
  
  forge: Modify claims and sign with a known secret
  Example: python3 masquerade.py forge -t <token> -c "role=admin" -s "secret"
  
  Bypass signature verification using alg: none
  Example: python3 masquerade.py none -t <token>
  
  kid: Inject or modify the kid header parameter
  Example: python3 masquerade.py kid -t <token> -k "../../dev/null"

  credits: Show tool credits and author info 
  Example: python3 masquerade.py credits
  
  help: Display this help menu
  Example: python3 masquerade.py help

  Installation

Clone the repository and ensure you are using Python 3:
Bash

git clone [https://github.com/yourusername/masquerade.git](https://github.com/yourusername/masquerade.git)
cd masquerade
python3 masquerade.py help

DISCLAIMER
This is simply a learning project. That being said the misuse of this tool in any way is out of my control and any impacts fall solely on the user.
