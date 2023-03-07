from unidecode import unidecode
import string
import os


def read_file(l_file_name: str) -> list:
    with open(l_file_name, 'r', encoding='UTF-8') as l_file:
        return l_file.readlines()


def letter_frequency_analysis(char_list: (list, str), text: str) -> dict[int, tuple[int, str]]:
    l_count_dict = {}
    for char in char_list:
        l_count_dict[char] = (text.count(char), str(round(text.count(char) / len(text), 3))+'%')
    return l_count_dict


def analyse_files(l_alphabet: (str, list), l_file_list: (str, list)) -> None:
    for l_file_name in l_file_list:
        if l_file_name.endswith('.txt'):
            l_to_decrypt = read_file(l_file_name)[0]
            print(f'File {l_file_name}, {len(l_to_decrypt)} characters:')
            print(letter_frequency_analysis(l_alphabet, l_to_decrypt))


if __name__ == '__main__':
    alphabet = [char.upper() for char in [*string.ascii_lowercase]]
    file_list = ['tekst1.txt', 'tekst2.txt']
    analyse_files(alphabet, file_list)
