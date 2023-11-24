import hashlib
import os
import re
import secrets
from base64 import b64encode, b64decode
from io import open
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12
import GUI

# Check if station is alive
def checkStation(ipaddr):
    ret = os.system("ping " + ipaddr)
    if ret != 0:
        return True
    else:
        return False


# Writing bytes to file
def writeToFile(Path, data):
    with open(Path, "wb") as f:
        f.write(data)


def getPasswd():
    global passToCert
    if passToCert == "":
        passwd = input()
    else:
        passwd = passToCert

    passToCert = passwd
    return passToCert.encode()


# Reading bytes to file
def readFile(Path):
    with open(Path, "rb") as f:
        return f.read()

# Encrypting file data with AES, AES key generation
def encryptAES(password, plain_text):
    # generate a random salt
    salt = get_random_bytes(AES.block_size)
    global Aes_private_key
    Aes_private_key = hashlib.scrypt(
        password, salt=salt, n=2 ** 14, r=8, p=1, dklen=32)

    print("AES PRIVATE KEY: " + b64encode(Aes_private_key).decode())
    cipher_config = AES.new(Aes_private_key, AES.MODE_GCM)
    cipher_text, tag = cipher_config.encrypt_and_digest(plain_text)
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }


# Decrypting data with AES
def decryptAES(enc_dict):
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])
    Aes_private_key = b64decode(enc_dict['pass'])

    cipher = AES.new(Aes_private_key, AES.MODE_GCM, nonce=nonce)

    return cipher.decrypt_and_verify(cipher_text, tag)

# Loading .p12 certificate
def loadCert(path):
    with open(path, "rb") as f:
        private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(f.read(), getPasswd())

    return private_key, certificate


# Encrypting data with .p12 cert
def encryptDataWithCert(data, certPath):
    private_key, certificate = loadCert(certPath)
    return certificate.public_key().encrypt(data.encode(),
                                            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                         algorithm=hashes.SHA256(),
                                                         label=None))


# Decrypt data with .p12 cert
def decryptWithCert(data, cert):
    private_key, certificate = loadCert(cert)
    return private_key.decrypt(data,
                               padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                            algorithm=hashes.SHA256(),
                                            label=None)).decode()


# Decrypting received data
def decryptDataFinal(data, password, Path_of_cert):
    with open(Path_of_cert, "rb") as f:
        private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(f.read(), password.encode())

    test = re.findall(r"[a-zA-Z0-9+/={1,2}]+", data)
    cipher_text = test[0]
    cipher_key = test[2]

    GUI.logging += f"Decrypting AES key.\n"

    keyToAES = private_key.decrypt(b64decode(cipher_key),
                                   padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                algorithm=hashes.SHA256(),
                                                label=None)).decode()

    print("Decrypted string with cert: " + keyToAES)

    regexForPrivateKey = r"(?:Private key: )([^\r\n]+)(?:; Tag: )([^\r\n]+)(?:; Nonce: )([^\r\n]+)"
    aaa = re.split(regexForPrivateKey, keyToAES)
    dict_keys = {
        'pass': aaa[1],
        'cipher_text': cipher_text,
        'nonce': aaa[3],
        'tag': aaa[2]
    }
    
    GUI.logging += f"Decrypting message.\n"
    decrypted = decryptAES(dict_keys)
    GUI.logging += f"Success!\n"
    return decrypted


# Encrypting data and preparation for sending
def encryptDataFinal(data, cert):
    generatedPass = secrets.token_bytes(20)
    encrypted = encryptAES(generatedPass, data)

    StringToEncrypt = "Private key: " + b64encode(Aes_private_key).decode("utf-8") + "; Tag: " + encrypted[
        'tag'] + "; Nonce: " + encrypted['nonce']
    print("String to encode: " + StringToEncrypt)

    print(StringToEncrypt)

    encrypted_AES_key = cert.public_key().encrypt(StringToEncrypt.encode(),
                                                  padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                               algorithm=hashes.SHA256(),
                                                               label=None))

    print("Encrypted string with cert: " + b64encode(encrypted_AES_key).decode())

    return encrypted['cipher_text'] + "\n============\n" + b64encode(encrypted_AES_key).decode()