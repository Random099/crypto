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


def freq_decrypt(l_alphabet: (str, list), l_todecrypt_filename: str, l_freq_filename: str) -> None:
    l_text = read_file(l_todecrypt_filename)[0]
    l_letters_freq = read_file(l_freq_filename)
    l_todecrypt_freq = letter_frequency_analysis(l_alphabet, l_text)
    l_language_freq = get_freq_dict(l_letters_freq)
    l_replace_map = {}
    for l_char, l_char_freq in l_language_freq.items():
        for l_char_toreplace, l_count_freq in l_todecrypt_freq.items():
            if round(abs(l_char_freq - l_count_freq[1]), 3) < 0.7:
                if l_char_toreplace not in list(l_replace_map.keys()):
                    l_replace_map[l_char_toreplace] = (l_char, round(abs(l_char_freq - l_count_freq[1]), 3))
                elif round(abs(l_char_freq - l_count_freq[1]), 3) < l_replace_map[l_char_toreplace][1]:
                    l_replace_map[dict_key_from_value(l_replace_map, l_replace_map[l_char_toreplace])] = (dict_key_from_value(l_replace_map, l_replace_map[l_char_toreplace]), 100)
                    l_replace_map[l_char_toreplace] = (l_char, round(abs(l_char_freq - l_count_freq[1]), 3))
    l_text = ''.join([l_replace_map[char][0] if char in list(l_replace_map.keys()) else char for char in l_text])
    write_file('replaced.txt', l_text)
    print(l_replace_map)


if __name__ == '__main__':
    alphabet = [char.upper() for char in [*string.ascii_lowercase]]
    #file_list = ['tekst1.txt', 'tekst2.txt']
    #analyse_files(alphabet, file_list)
    freq_decrypt(alphabet, 'tekst2.txt', 'english_letter_frequency.txt')
