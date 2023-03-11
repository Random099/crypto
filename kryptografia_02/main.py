from unidecode import unidecode
import string
import copy
import random


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


def freq_decrypt(l_alphabet: (str, list), l_todecrypt: str, l_freq_filename: str) -> (dict, list, str):
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
    return replace_pairs, pair_diff, l_text


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


def swap_letters(alphabet: (str, list)) -> dict[str, str]:
    swap_map = dict()
    while True:
        try:
            original_letter = input('Letter to swap:\n')
            if original_letter == '?':
                break
            swapto_letter = input('Letter after swap:\n')
            if swapto_letter == '?':
                break
            if original_letter not in alphabet or swapto_letter not in alphabet:
                raise Warning('Not a valid character')
            swap_map[original_letter] = swapto_letter
        except Warning as err:
            print(str(err))
    return swap_map


def gen_random_key(alphabet: (str, list)) -> dict[str, str]:
    alphabet_to = alphabet[:]
    random.shuffle(alphabet_to)
    return dict(zip(alphabet, alphabet_to))


def merge_entries(to_change: dict, source: dict) -> dict:
    for key, value in source.items():
        at_value = dict_key_from_value(to_change, value)
        temp = to_change[key]
        to_change[key] = source[key]
        to_change[at_value] = temp
    return to_change


def update_key(old_key: dict, to_keep: dict) -> dict[str, str]:
    to_shuffle = {key: value for key, value in old_key.items() if key not in to_keep.keys()}
    to_shuffle_values = list(to_shuffle.values())
    random.shuffle(list(to_shuffle_values))
    shuffled = dict(zip(list(to_shuffle.keys()), to_shuffle_values))
    return to_keep | shuffled


def get_keep_list(elements: dict) -> dict:
    while True:
        try:
            to_keep = [*input('Elements to keep:')]
            print(to_keep)
            for element in to_keep:
                if element == '?':
                    break
                if element not in list(elements.keys()):
                    raise Warning('Not in given list')
            return {key: value for key, value in elements.items() if key in to_keep}
        except Warning as err:
            print(str(err))


def attempt_decrypt(text: str, key: dict) -> str:
    return ''.join([key[char] if char in key.keys() else char for char in text])


def ngram_list_decrypt(ngram_list: list, key: dict):
    temp_ngram_list = copy.deepcopy(ngram_list)
    for i in range(len(temp_ngram_list)):
        temp_ngram_list[i] = ''.join([key[char] for char in temp_ngram_list[i]])
    return temp_ngram_list


def words_in_text(word_list: list, text: str, word_count: int, unique_words: set) -> bool:
    for word in word_list:
        if word in text:
            unique_words.add(word)
        if len(unique_words) == word_count:
            return True
    return False


def get_to_keep(letter_map: dict, words: set, exclude: dict) -> dict:
    new_map = dict()
    for word in words:
        for letter in word:
            if letter in letter_map.keys() and letter not in exclude.keys():
                new_map[letter] = letter_map[letter]
    return new_map | exclude


def format_text(text: str, func):  # Formats the text into 5-letter words and 7 columns
    for word in text:
        func(word+'\n')


def write_file_2(l_file_name: str, text: str):
    with open(l_file_name, 'w') as file:
        format_text(text, file.write)
    return l_file_name

if __name__ == '__main__':
    ALPHABET = [char.upper() for char in [*string.ascii_lowercase]]
    LANGUAGE = 'english'
    SAMPLE_WORDS = [unidecode(word.strip()).upper() for word in read_file(f'{LANGUAGE}_sample_words.txt')]
    SAMPLE_WORDS += [unidecode(word.strip()).upper() for word in read_file(f'english_sample_words.txt')]
    SAMPLE_WORDS += [word.upper()[:-2] for word in read_file(f'polish_sample_words_2.txt') if word not in SAMPLE_WORDS]
    SAMPLE_WORDS += [word for word in read_file(f'english_cleared.txt') if word not in SAMPLE_WORDS]
    SAMPLE_WORDS = [word for word in SAMPLE_WORDS if len(word) > 3]
    ENCRYPTED_TEXT_FILE = 'tekst2.txt'
    ENCRYPTED_TEXT = read_file(ENCRYPTED_TEXT_FILE)[0]
    bigram_freq = get_ngram_freq(ENCRYPTED_TEXT, 2)
    trigram_freq = get_ngram_freq(ENCRYPTED_TEXT, 3)
    #quadrigram_freq = get_ngram_freq(ENCRYPTED_TEXT, 4)
    top_10_bigrams = list(bigram_freq.items())[-10:]  # Top 10 highest frequency bigrams
    top_10_bigrams = [x[0] for x in top_10_bigrams]
    print(top_10_bigrams)
    top_10_trigrams = list(trigram_freq.items())[-10:]  # Top 10 highest frequency trigrams
    top_10_trigrams = [x[0] for x in top_10_trigrams]
    print(top_10_trigrams)
    #FREQ_ATTEMPTED_KEY, PAIR_DIFF, FREQ_DECRYPT_TEXT = freq_decrypt(ALPHABET, ENCRYPTED_TEXT, f'{LANGUAGE}_letter_frequency.txt')
    #TO_KEEP = {'M': 'N', 'D': 'I', 'A': 'E', 'O': 'W', 'W': 'O', 'N': 'L', 'C': 'A'}
    TO_KEEP = dict()
    COUNTER = 0
    START_TARGET_WORD_COUNT = 20
    TARGET_WORD_COUNT = START_TARGET_WORD_COUNT
    while True:
        COUNTER += 1
        UNIQUE_WORDS = set()
        if COUNTER > 50:
            TARGET_WORD_COUNT = START_TARGET_WORD_COUNT
            print(TARGET_WORD_COUNT)
            print(f'KEY RESET')
            CURRENT_KEY = gen_random_key(ALPHABET)
            COUNTER = 0
        CURRENT_KEY = update_key(gen_random_key(ALPHABET), TO_KEEP)
        DECRYPTED_TEXT = attempt_decrypt(ENCRYPTED_TEXT[:10000], CURRENT_KEY)
        if words_in_text(SAMPLE_WORDS, DECRYPTED_TEXT, TARGET_WORD_COUNT, UNIQUE_WORDS):
            TARGET_WORD_COUNT += 1
            TO_KEEP = get_to_keep(CURRENT_KEY, UNIQUE_WORDS, TO_KEEP)
            print(TO_KEEP)
            DECRYPTED_TEXT = attempt_decrypt(ENCRYPTED_TEXT, CURRENT_KEY)
            print(f'Text sample: {DECRYPTED_TEXT[0:200]}')
            #break
        if len(TO_KEEP) == len(ALPHABET)-2:
            print(f'DONE')
            print(UNIQUE_WORDS)
            break
    write_file('attempted_decrypt.txt', DECRYPTED_TEXT)
    while True:
        to_exit = input(f'Input "EXIT" to get the final key:\n')
        if to_exit == 'EXIT':
            print(f'FINAL KEY: {CURRENT_KEY}')
            break
        else:
            pass
        print(f'Text sample: {DECRYPTED_TEXT[0:200]}')
        print(CURRENT_KEY)
        print(f'Top 10 ogbigrams: {top_10_bigrams}')
        print(f'Top 10 bigrams: {ngram_list_decrypt(top_10_bigrams, CURRENT_KEY)}')
        print(f'Top 10 ogtrigrams: {top_10_trigrams}')
        print(f'Top 10 bigrams: {ngram_list_decrypt(top_10_trigrams, CURRENT_KEY)}')
        print(f'Letter: {list(CURRENT_KEY.keys())}')
        print(f'Swapto: {list(CURRENT_KEY.values())}')
        SWAP_MAP = swap_letters(ALPHABET)
        CURRENT_KEY = merge_entries(CURRENT_KEY, SWAP_MAP)
        KEPT_KEYS = get_keep_list(CURRENT_KEY)
        CURRENT_KEY = update_key(CURRENT_KEY, KEPT_KEYS)
        DECRYPTED_TEXT = attempt_decrypt(ENCRYPTED_TEXT, CURRENT_KEY)
        write_file('attempted_decrypt.txt', DECRYPTED_TEXT)

