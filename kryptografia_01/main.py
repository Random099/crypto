from unidecode import unidecode
import os
import string
import ciphers


class Cipher:
    def __init__(self, _plaintext: str, _alphabet: dict):
        self.plaintext = _plaintext
        self.alphabet = _alphabet

    def encrypt(self, l_cipher_type: str, cipher_func_extra_args, *args) -> str:  # Encrypts the text with given function(cipher)
        encryption_procedure = ciphers.cipher_list().get(l_cipher_type)('encrypt', *cipher_func_extra_args)
        return ''.join([encryption_procedure(character, *args) for character in self.prepare_text()]).upper()

    def decrypt(self, l_cipher_type: str, cipher_func_extra_args, *args) -> str:  # Decrypts the text with given function(cipher)
        decryption_procedure = ciphers.cipher_list().get(l_cipher_type)('decrypt', *cipher_func_extra_args)
        return ''.join([decryption_procedure(character, *args) for character in self.prepare_text()]).lower()

    def prepare_text(self) -> str:  # Prepares the text for encrypting/decrypting
        no_diacritics_lower = unidecode(self.plaintext).lower()
        return ''.join([char for char in no_diacritics_lower if char in list(self.alphabet.values())])


def format_text(text: str, func):  # Formats the text into 5-letter words and 7 columns
    split_array = [text[i:i + 5] for i in range(0, len(text), 5)]
    for i in range(0, len(split_array), 7):
        func(' '.join(split_array[i:i + 7])+'\n')


def write_file(l_file_name: str, text: str):
    with open(l_file_name, 'w') as file:
        format_text(text, file.write)
    return l_file_name


def choose_file(message: str, cond=None) -> str:
    while True:
        try:
            l_file_name = input(f'Input the name of the file {message}\n')
            if l_file_name == '':
                return 'demo.txt'
            elif l_file_name == cond:
                return cond
            elif l_file_name+'.txt' not in os.listdir(os.path.abspath(os.getcwd())):
                raise Warning(f'No such file in {os.path.abspath(os.getcwd())}')
            else:
                return l_file_name + '.txt'
        except Warning as err:
            print(str(err))


def read_file(l_file_name: str) -> list:
    with open(l_file_name, 'r', encoding='UTF-8') as file:
        return file.readlines()


def choose_option(option_list: (tuple, list, dict), message: str, cond=None):
    if isinstance(option_list, (tuple, list)):
        while True:
            try:
                option_enum = input(message+'\n')
                if option_enum == cond:
                    return cond
                elif option_enum not in option_list:
                    raise Warning(f'No such option in the given list')
                else:
                    return option_enum
            except Warning as err:
                print(str(err))
    if isinstance(option_list, dict):
        while True:
            try:
                option_enum = input(message+'\n')
                if option_enum == cond:
                    return cond
                elif option_enum not in option_list.keys():
                    raise Warning(f'No such option in the given list')
                else:
                    return option_list.get(option_enum)
            except Warning as err:
                print(str(err))


def get_input(l_available_ciphers: dict, l_alphabet: dict):  # Handles getting input from the user (file to be encrypted, decrypted and cipher type)
    return_list = {'run_mode': choose_option(['1', '2', '3'], 'What do you want to do(input "?" to end)\n'
                        '1 - Encrypt a file\n2 - Decrypt a file\n3 - Demonstrate encryption and decryption', '?')}
    if return_list.get('run_mode') == '?':
        return return_list
    return_list['file_name'] = choose_file('containing the plaintext(press enter to use demo file)')
    plaintext = ''.join(read_file(return_list['file_name']))
    return_list['to_encrypt'] = Cipher(plaintext, l_alphabet)
    return_list['cipher_type'] = choose_option(l_available_ciphers, f'Choose the cipher'
                                    f'(Input a number corresponding to the cipher).'
                                    f'\nAvailable ciphers:\n1 - Atbash\n2 - ROT13\n3 - Caesar\'s\n4 - Gaderypoluki')
    if return_list['cipher_type'] == 'Caesar\'s':
        while True:
            try:
                shift = input(f'Give shift for the Caesar\'s cipher (-26:26)\n')
                if int(float(shift)) > 25 or int(float(shift)) < -25:
                    raise Warning(f'Shift must be in (-26:26)')
                else:
                    if not float(shift).is_integer():
                        print(f'Shift has been rounded down to {int(float(shift))}')
                    return_list['shift'] = int(float(shift))
                    break
            except Warning as err:
                print(str(err))
    if return_list['cipher_type'] == 'ROT13':  # In ROT13 case the program performs Caesar's cipher with shift = 13
        return_list['cipher_type'] = 'Caesar\'s'
        return_list['shift'] = 13
    return return_list


if __name__ == '__main__':
    available_ciphers = {'1': 'Atbash', '2': 'ROT13', '3': 'Caesar\'s', '4': 'Gaderypoluki'}
    alphabet = dict(zip([x for x in range(26)], [*string.ascii_lowercase]))  # Alphabet dict (position mapped with letter)
    cipher_extra_args = {'Atbash': [alphabet], 'ROT13': [], 'Caesar\'s': [alphabet], 'Gaderypoluki': []}
    while True:
        user_input = get_input(available_ciphers, alphabet)
        if user_input.get('run_mode') == '?':  # Stop program on '?' input
            break
        cipher_parameters = [i for i in tuple(user_input.values())[4:]]  # Create a list of parameters for the given cipher
        if user_input['run_mode'] == '1':
            encrypted = user_input['to_encrypt'].encrypt(user_input['cipher_type'], cipher_extra_args[user_input['cipher_type']], *cipher_parameters)
            encrypted_file_name = write_file(user_input['file_name'][:-4] + '_encrypted.txt', encrypted)
        elif user_input['run_mode'] == '2':
            to_decrypt = Cipher(''.join(read_file(user_input['file_name'])), alphabet)
            decrypted = to_decrypt.decrypt(user_input['cipher_type'], cipher_extra_args[user_input['cipher_type']], *cipher_parameters)
            decrypted_file_name = write_file(user_input['file_name'][:-4] + '_decrypted.txt', decrypted)
        elif user_input['run_mode'] == '3':
            encrypted = user_input['to_encrypt'].encrypt(user_input['cipher_type'], cipher_extra_args[user_input['cipher_type']], *cipher_parameters)  # String of encrypted text
            encrypted_file_name = write_file(user_input['file_name'][:-4]+'_encrypted.txt', encrypted)  # Write the string to file and assign its name to variable
            to_decrypt = Cipher(''.join(read_file(encrypted_file_name)), alphabet)  # Object of type Cipher containing text to be decrypted
            decrypted = to_decrypt.decrypt(user_input['cipher_type'], cipher_extra_args[user_input['cipher_type']], *cipher_parameters)  # String of decrypted text
            decrypted_file_name = write_file(user_input['file_name'][:-4]+'_decrypted.txt', decrypted)  # Write the string to file
