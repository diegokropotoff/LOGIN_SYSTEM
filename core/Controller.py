from Model import Pessoa, Session
import re
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

class AESCipher(object):
    def __init__(self, key):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    
    def __pad(self, plain_text):
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text
    
    @staticmethod
    def __unpad(plain_text):
        last_character = plain_text[len(plain_text)-1:]
        bytes_to_remove = ord(last_character)
        return plain_text[:-bytes_to_remove]
    

    def encrypt(self, plain_text):
        plain_text = self.__pad(plain_text)
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8")
    

    def decrypt(self, encrypted_text):
        encrypted_text = b64decode(encrypted_text)
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
        return self.__unpad(plain_text)

class ControllerPessoa:
    def valida_email(self, email):
        email = email.lower()
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex, email):
            return True
        else: 
            return False
        
    def valida_senha(self, senha):
        if len(senha) < 8 and len(senha) > 25:
            print('Use uma senha de 8-25 caracteres')
            return False
        elif re.search('[ ]', senha):
            print('Não use espaços')
            return False
        elif not re.search('[A-Z]', senha):
            print('Use letras maiúsculas')
            return False
        elif not re.search('[0-9]', senha):
            print('Use números')
            return False
        elif not re.search('[@#$%&ˆ*_]', senha):
            print('Use caracteres especiais')
            return False
        else:
            return True


    def cadastro(self, nome_usuario, email_usuario, senha):
        session = Session()
        aes = AESCipher('minhachavequeehumasenha')

        email_existe = list(session.query(Pessoa).filter(Pessoa.email == email_usuario))

        if len(email_existe) > 0:
            print('Email já cadastrado.')
        else:
            if not self.valida_email(email_usuario):
                print('Email inválido!')

            else:
                while not self.valida_senha(senha):
                    senha = input('Senha: ')
                senha_crypto = aes.encrypt(senha)
                session.add(Pessoa(nome = nome_usuario, email = email_usuario, senha = senha_crypto))
                session.commit()


    def login(self, email_usuario, senha):
        session = Session()
        usuario = session.query(Pessoa).filter(Pessoa.email == email_usuario).first()
        if usuario is None:
            print('Email não cadastrado')
        else:
            aes = AESCipher('minhachavequeehumasenha')
            senha_usuario = aes.decrypt(usuario.senha)
            
            if senha == senha_usuario:
                print(f'Login executado com sucesso!\nBem-Vindo de volta {usuario.nome}')

            else:
                print('Senha inválida!')