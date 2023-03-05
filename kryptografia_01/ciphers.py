# Functions responsible for specific ciphers

def cipher_list():
    return {'Atbash': ciphert_atbash, 'Caesar\'s': ciphert_caesar, 'Gaderypoluki': ciphert_gaderypoluki}


def ciphert_caesar(operation: str, alphabet: dict) -> chr:
    if operation == 'encrypt':
        return lambda character, shift: alphabet.get((ord(character) - 97 + shift) % len(alphabet))
    elif operation == 'decrypt':
        return lambda character, shift: alphabet.get((ord(character) - 97 - shift) % len(alphabet))


def ciphert_atbash(operation: str, alphabet: dict) -> chr:
    if operation == 'encrypt' or operation == 'decrypt':
        return lambda character: alphabet.get(((len(alphabet)-1) * (ord(character) - 96) % len(alphabet)))


def ciphert_gaderypoluki(operation: str) -> chr:
    gaderypoluki_str = 'GADERYPOLUKI'
    gaderypoluki_str_swapped = 'AGEDYROPULIK'
    if operation == 'encrypt' or operation == 'decrypt':
        return lambda character: gaderypoluki_str_swapped[gaderypoluki_str.index(character.upper())] \
            if character.upper() in 'GADERYPOLUKI' else character
