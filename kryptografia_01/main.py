from unidecode import unidecode
import os
import string


class Cipher:
    alphabet = dict(zip([x for x in range(26)], [*string.ascii_lowercase])) #Alphabet dict (position mapped with letter)
    available_ciphers = {'1': 'Atbash', '2': 'ROT13', '3': 'Caesar\'s'}

    def __init__(self, plaintext: str):
        self.plaintext = plaintext

    @staticmethod
    def ciphert_caesar(character: chr, shift: int) -> chr:
        return Cipher.alphabet.get((ord(character)-97 + shift) % 26)

    def prepare_text(self) -> list: #Prepares the text for encrypting/decrypting
        return [letter for letter in unidecode(self.plaintext).lower() if letter in list(Cipher.alphabet.values())]

    def encrypt(self, l_cipher_type, *args) -> str: #Encrypts the text with given function(cipher)
        print(self.prepare_text())
        encryption_procedures = {'Atbash': 'Atbash', 'ROT13': 'ROT13', 'Caesar\'s': Cipher.ciphert_caesar}
        return ''.join([encryption_procedures.get(l_cipher_type)(character, *args) for character in self.prepare_text()]).upper()

    def decrypt(self, l_cipher_type, *args) -> str: #Decrypts the text with given function(cipher)
        decryption_procedures = {'Atbash': 'Atbash', 'ROT13': 'ROT13', 'Caesar\'s': Cipher.ciphert_caesar}
        return ''.join([decryption_procedures.get(l_cipher_type)(character, *args) for character in self.prepare_text()])


def format_text(text: str, func): #Formats the text into 5 letter words and 7 columns
    split_array = [text[i:i + 5] for i in range(0, len(text), 5)]
    for i in range(0, len(split_array), 7):
        func(' '.join(split_array[i:i + 7])+'\n')


def write_file(l_file_name: str, text: str):
    with open(l_file_name, 'w') as file:
        format_text(text, file.write)
    return l_file_name


def choose_file(message: str) -> str:
    while True:
        print(f'Input the name of the file {message}')
        try:
            l_file_name = input()
            if l_file_name == '':
                return 'demo.txt'
            elif l_file_name+'.txt' not in os.listdir(os.path.abspath(os.getcwd())):
                raise Warning(f'No such file in {os.path.abspath(os.getcwd())}')
            else:
                return l_file_name + '.txt'
        except Warning as err:
            print(str(err))


def read_file(l_file_name: str) -> list:
    with open(l_file_name, 'r', encoding='UTF-8') as file:
        return file.readlines()


def choose_option(option_list, message: str):
    if isinstance(option_list, (tuple, list)):
        while True:
            try:
                print(message)
                option_enum = input()
                print(option_enum)
                if option_enum not in option_list:
                    raise Warning(f'No such option in the given list')
                else:
                    return option_enum
            except Warning as err:
                print(str(err))
    if isinstance(option_list, dict):
        while True:
            try:
                print(message)
                option_enum = input()
                if option_enum not in option_list.keys():
                    raise Warning(f'No such option in the given list')
                else:
                    return option_list.get(option_enum)
            except Warning as err:
                print(str(err))


def get_input(): #Handles getting input from the user (file to be encrypted, decrypted and cipher type)
    l_file_name = choose_file('containing the plaintext')
    plaintext = ''.join(read_file(l_file_name))
    l_to_encrypt = Cipher(plaintext)
    l_cipher_type = choose_option(Cipher.available_ciphers, f'Choose the cipher to be used to encrypt the chosen file '
                                    f'(Input a number corresponding to the cipher).'
                                    f'\nAvailable ciphers:\n1 - Atbash\n2 - ROT13\n3 - Caesar\'s')
    return l_to_encrypt, l_cipher_type, l_file_name

#test_text = "AĄbĆ!!    ++BÓłAaa+aa+aaaaaaaaaaaaaaaaaaaaAAAaaaaaaaaaaaaaaaaaaabbcccccccccccccccccccccccccccccccccccc"


if __name__ == '__main__':
    #print(os.listdir(os.path.abspath(os.getcwd())))
    to_encrypt, cipher_type, to_encrypt_file_name = get_input()
    #print(to_encrypt.plaintext, cipher_type, to_encrypt_file_name)
    encrypted = to_encrypt.encrypt(cipher_type, 13)
    encrypted_file_name = write_file(to_encrypt_file_name[0:len(to_encrypt_file_name)-4]+'_encrypted.txt', encrypted)
    to_decrypt = Cipher(''.join(read_file(encrypted_file_name)))
    decrypted = to_decrypt.decrypt(cipher_type, 13)
    decrypted_file_name = write_file(to_encrypt_file_name[0:len(to_encrypt_file_name)-4]+'_decrypted.txt', decrypted)