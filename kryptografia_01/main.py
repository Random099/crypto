from unidecode import unidecode
import os
import string


class Cipher:
    alphabet = dict(zip([x for x in range(26)], [*string.ascii_lowercase])) #Alphabet dict (position mapped with letter)
    available_ciphers = {'1': 'Atbash', '2': 'ROT13', '3': 'Caesar\'s'}

    def __init__(self, plaintext: str):
        self.plaintext = plaintext

    @staticmethod
    def ciphert_caesar(operation) -> chr:
        if operation == 'encrypt':
            return lambda character, shift: Cipher.alphabet.get((ord(character)-97 + shift) % 26)
        elif operation == 'decrypt':
            return lambda character, shift: Cipher.alphabet.get((ord(character)-97 - shift) % 26)

    @staticmethod
    def ciphert_atbash(operation) -> chr:
        if operation == 'encrypt' or operation == 'decrypt':
            return lambda character: Cipher.alphabet.get((25*(ord(character)-96) % 26))

    def prepare_text(self) -> list: #Prepares the text for encrypting/decrypting
        return [letter for letter in unidecode(self.plaintext).lower() if letter in list(Cipher.alphabet.values())]

    def encrypt(self, l_cipher_type, *args) -> str: #Encrypts the text with given function(cipher)
        print(self.prepare_text())
        encryption_procedures = {'Atbash': Cipher.ciphert_atbash, 'ROT13': Cipher.ciphert_caesar, 'Caesar\'s': Cipher.ciphert_caesar}
        encryption_procedure = encryption_procedures.get(l_cipher_type)('encrypt')
        return ''.join([encryption_procedure(character, *args) for character in self.prepare_text()]).upper()

    def decrypt(self, l_cipher_type, *args) -> str: #Decrypts the text with given function(cipher)
        decryption_procedures = {'Atbash': Cipher.ciphert_atbash, 'ROT13': Cipher.ciphert_caesar, 'Caesar\'s': Cipher.ciphert_caesar}
        decryption_procedure = decryption_procedures.get(l_cipher_type)('decrypt')
        return ''.join([decryption_procedure(character, *args) for character in self.prepare_text()])


def format_text(text: str, func): #Formats the text into 5 letter words and 7 columns
    split_array = [text[i:i + 5] for i in range(0, len(text), 5)]
    for i in range(0, len(split_array), 7):
        func(' '.join(split_array[i:i + 7])+'\n')


def write_file(l_file_name: str, text: str):
    with open(l_file_name, 'w') as file:
        format_text(text, file.write)
    return l_file_name


def choose_file(message: str, quit = None) -> str:
    while True:
        try:
            l_file_name = input(f'Input the name of the file {message}\n')
            if l_file_name == '':
                return 'demo.txt'
            elif l_file_name == quit:
                return quit
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
                option_enum = input(message+'\n')
                if option_enum not in option_list:
                    raise Warning(f'No such option in the given list')
                else:
                    return option_enum
            except Warning as err:
                print(str(err))
    if isinstance(option_list, dict):
        while True:
            try:
                option_enum = input(message+'\n')
                if option_enum not in option_list.keys():
                    raise Warning(f'No such option in the given list')
                else:
                    return option_list.get(option_enum)
            except Warning as err:
                print(str(err))


def get_input(): #Handles getting input from the user (file to be encrypted, decrypted and cipher type)
    return_list = {'file_name': choose_file('containing the plaintext or input "?" to end', '?')}
    if return_list.get('file_name')[0] == '?':
        return return_list
    plaintext = ''.join(read_file(return_list['file_name']))
    return_list['to_encrypt'] = Cipher(plaintext)
    return_list['cipher_type'] = choose_option(Cipher.available_ciphers, f'Choose the cipher to be used to encrypt the chosen file '
                                    f'(Input a number corresponding to the cipher).'
                                    f'\nAvailable ciphers:\n1 - Atbash\n2 - ROT13\n3 - Caesar\'s')
    if return_list['cipher_type'] == 'Caesar\'s':
        while True:
            try:
                shift = input(f'Give shift for the Caesar\'s cipher (-26:26)\n')
                if int(shift) > 25 or int(shift) < -25:
                    raise Warning(f'Shift must be between in (-26:26)')
                else:
                    return_list['shift'] = int(shift)
                    break
            except Warning as err:
                print(str(err))
    if return_list['cipher_type'] == 'ROT13':
        return_list['shift'] = 13
    return return_list


if __name__ == '__main__':
    while True:
        user_input = get_input()
        if user_input.get('file_name')[0] == '?':
            break
        cipher_parameters = [i for i in tuple(user_input.values())[3:]] # Create a list of parameters for the given cipher
        print(cipher_parameters)
        encrypted = user_input['to_encrypt'].encrypt(user_input['cipher_type'], *cipher_parameters)
        encrypted_file_name = write_file(user_input['file_name'][0:len(user_input['file_name'])-4]+'_encrypted.txt', encrypted)
        to_decrypt = Cipher(''.join(read_file(encrypted_file_name)))
        decrypted = to_decrypt.decrypt(user_input['cipher_type'], *cipher_parameters)
        decrypted_file_name = write_file(user_input['file_name'][0:len(user_input['file_name'])-4]+'_decrypted.txt', decrypted)