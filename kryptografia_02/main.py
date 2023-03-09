from unidecode import unidecode
import string
import os


def dict_key_from_value(l_dict: dict, target_value):
    keys = [key for key, value in l_dict.items() if value == target_value]
    if keys:
        return keys[0]
    return None


def read_file(l_file_name: str) -> list:
    with open(l_file_name, 'r', encoding='UTF-8') as l_file:
        return l_file.readlines()


def write_file(l_file_name: str, l_text: (str, bytes)) -> None:
    with open(l_file_name, 'w') as l_file:
        l_file.write(l_text)


def letter_frequency_analysis(l_char_list: (list, str), l_text: (str, list)) -> dict[int, tuple[int, float]]:
    l_count_dict = {}
    for char in l_char_list:
        l_count_dict[char] = (l_text.count(char), round((l_text.count(char) / len(l_text))*100, 3))
    return l_count_dict


def analyse_files(l_alphabet: (str, list), l_file_list: (str, list)) -> None:
    for l_file_name in l_file_list:
        if l_file_name.endswith('.txt'):
            l_to_decrypt = read_file(l_file_name)[0]
            print(f'File {l_file_name}, {len(l_to_decrypt)} characters:')
            print(letter_frequency_analysis(l_alphabet, l_to_decrypt))


def get_freq_dict(l_text: (str, list)) -> dict[chr, float]:
    l_letters = [line[0].upper() for line in l_text[1:]]
    l_percentages = [float(line[2:-1]) for line in l_text[1:]]
    l_freq_dict = dict(zip(l_letters, l_percentages))
    for letter, percentage in list(l_freq_dict.items())[26:]:  # Remove diacritics and sum percentages
        ascii_letter = unidecode(letter).upper()
        if ascii_letter in list(l_freq_dict.keys())[:26]:
            l_freq_dict[ascii_letter] += l_freq_dict[letter]
    for key in list(l_freq_dict.keys())[26:]:  # Remove redundant dict items
        del l_freq_dict[key]
    return l_freq_dict


def get_pair(dict_1: dict, dict_2: dict):
    curr_min = float('inf')
    pair = []
    for key_1, value_1 in dict_1.items():
        for key_2, value_2 in dict_2.items():
            if abs(value_1 - value_2) < curr_min:
                curr_min = abs(value_1 - value_2)
                pair = [key_2, key_1]
    return pair


def freq_decrypt(l_alphabet: (str, list), l_todecrypt_filename: str, l_freq_filename: str) -> None:
    l_text = read_file(l_todecrypt_filename)[0]
    l_letters_freq = read_file(l_freq_filename)
    l_todecrypt_freq = {letter: frequency[1] for letter, frequency in letter_frequency_analysis(l_alphabet, l_text).items()}
    l_todecrypt_freq = dict(sorted(l_todecrypt_freq.items(), key=lambda item: item[1]))
    l_language_freq = get_freq_dict(l_letters_freq)
    l_language_freq = dict(sorted(l_language_freq.items(), key=lambda item: item[1]))
    replace_pairs = {}

    for letter in range(len(l_alphabet)):
        pair = get_pair(l_language_freq, l_todecrypt_freq)
        replace_pairs[pair[0]] = pair[1]
        del l_language_freq[pair[1]]
        del l_todecrypt_freq[pair[0]]
    print(replace_pairs)
    l_text = ''.join([replace_pairs[char] if char in list(replace_pairs.keys()) else char for char in l_text])
    write_file('replaced.txt', l_text)


if __name__ == '__main__':
    alphabet = [char.upper() for char in [*string.ascii_lowercase]]
    #file_list = ['tekst1.txt', 'tekst2.txt']
    #analyse_files(alphabet, file_list)
    freq_decrypt(alphabet, 'tekst2.txt', 'english_letter_frequency.txt')
