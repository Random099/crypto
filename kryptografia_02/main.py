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


def get_pair(dict_1: dict, dict_2: dict) -> list:
    curr_min = float('inf')
    pair = []
    for key_1, value_1 in dict_1.items():
        for key_2, value_2 in dict_2.items():
            if abs(value_1 - value_2) < curr_min:
                curr_min = abs(value_1 - value_2)
                pair = [key_2, key_1, curr_min]
    return pair


def freq_decrypt(l_alphabet: (str, list), l_todecrypt: str, l_freq_filename: str) -> (dict, list):
    l_letters_freq = read_file(l_freq_filename)
    l_todecrypt_freq = {letter: frequency[1] for letter, frequency in letter_frequency_analysis(l_alphabet, l_todecrypt).items()}
    l_todecrypt_freq = dict(sorted(l_todecrypt_freq.items(), key=lambda item: item[1]))
    l_language_freq = get_freq_dict(l_letters_freq)
    l_language_freq = dict(sorted(l_language_freq.items(), key=lambda item: item[1]))
    replace_pairs = {}
    pair_diff = []

    for letter in range(len(l_alphabet)):
        pair = get_pair(l_language_freq, l_todecrypt_freq)
        replace_pairs[pair[0]] = pair[1]
        pair_diff.append(pair[2])
        del l_language_freq[pair[1]]
        del l_todecrypt_freq[pair[0]]
    l_text = ''.join([replace_pairs[char] if char in list(replace_pairs.keys()) else char for char in l_todecrypt])
    write_file('replaced.txt', l_text)
    return replace_pairs, pair_diff

def get_ngram_freq(text: str, n: int) -> dict:
    ngram_set = set()
    for i in range(len(text)-(n-1)):
        ngram_set.add(text[i:i + n])
    ngram_sum = 0
    for ngram in ngram_set:
        ngram_sum += text.count(ngram)
    ngram_freq = dict()
    for ngram in ngram_set:
        ngram_freq[ngram] = round(text.count(ngram) / ngram_sum, 4)
    return dict(sorted(ngram_freq.items(), key=lambda item: item[1]))


def swap_letters(alphabet: (str, list), file_name: str) -> dict[str, str]:
    text = read_file(file_name)
    swap_map = dict()
    while True:
        try:
            original_letter = input('Letter to swap:\n')
            swapto_letter = input('Letter after swap:\n')
            if original_letter or swapto_letter == '?':
                break
            elif original_letter or swapto_letter not in alphabet:
                raise Warning('Not a valid character')
            swap_map[original_letter] = swapto_letter
        except Warning as err:
            print(str(err))
    text = ''.join([swap_map[char] if char in list(swap_map.keys()) else char for char in text])
    write_file('after_swap.txt', text)
    return swap_map


if __name__ == '__main__':
    alphabet = [char.upper() for char in [*string.ascii_lowercase]]
    encrypted_text = read_file('tekst2.txt')[0]
    bigram_freq = get_ngram_freq(encrypted_text, 2)
    trigram_freq = get_ngram_freq(encrypted_text, 3)
    quadrigram_freq = get_ngram_freq(encrypted_text, 4)
    #print(list(bigram_freq.items())[-10:]) # Print 10 highest frequency bigrams
    #print(list(trigram_freq.items())[-10:]) # Print 10 highest frequency trigrams
    #print(list(quadrigram_freq.items())[-10:])  # Print 10 highest frequency quadrigrams
    attempted_key, pair_diff = freq_decrypt(alphabet, encrypted_text, 'english_letter_frequency.txt')
    while True:
        SWAP_MAP = swap_letters(alphabet, 'replaced.txt')
        for letter in SWAP_MAP.keys():
            attempted_key[letter] = SWAP_MAP[letter]
    #pair_chances = dict(zip([round(x, 4) for x in pair_diff], list(attempted_key.items())))
