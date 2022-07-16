from argparse import ArgumentParser
from random import shuffle
from pygtrans import Translate
from pygtrans import Null
from os import walk
from pathlib import *
from re import findall

def input_parse():
    """
    parse the input argvs:
    -n/--num <integer> : number of the words wanted, default value is 40
    -r/--random : if the words are random shuffled, true if -r is entered
    -s/--start <integer> : the start index of the words to select, default value is 0, 
                           will be reset to 1 if start index is larger than the size of the words or less than 1
    -l/--length <integer> : the length of the words to select, default value is 40, will be set to 1 if is less than 1
    -t/--total <integer> : the total number of the word books needed, defalut value is 1, will be set to 1 if is less than 1
    """
    input_parser = ArgumentParser(description = "Choose how the words are selected.")
    input_parser.add_argument('-n', '--num', type = int, default = 40, help = 'number of the words wanted, default value is 40')
    input_parser.add_argument('-r', '--random', action = 'store_true', help = 'if the words are random shuffled, true if -r is entered')
    input_parser.add_argument('-s', '--start', type = int, default = 0, help = 'the start index of the words to select, default value is 0')
    input_parser.add_argument('-l', '--length', type = int, default = 40, help = 'the length of the words to select, default value is 40')
    input_parser.add_argument('-t', '--total', type = int, default = 1, help = 'the total number of the word books needed, defalut value is 1')
    argvs = input_parser.parse_args()
    return argvs.num, argvs.random, argvs.start, argvs.length, argvs.total

def generate_wordbook(word_num: int, flag_random: bool, select_start_pos: int, select_length: int, book_num: int, book_index: int):
    """
    Function to generate wordbooks
    word_num: number of words selected
    flag_random: if the words are random shuffled
    select_start_pos: the started index to select words, will be reset to 0 if is larger than the size of the words minus 1 or less than 0
    select_length: the length of words to select (will be set to 1 if is less than 1), 
                   that is to say [select_start_pos, select_start_pos + select_length) is the range to select words,
                   and select_start_pos + select_length will no larger than the size of words
    book_num: the total number of the workbooks to generate, wll be set to 1 if less than 1
    book_index: the start_index of the generated wordbooks, depends on the largest index of the existed wordbook
    """
    with open('./collection.txt', 'r') as f:
        all_words = f.read().split('\n\n')
    if select_start_pos not in range(0, len(all_words)):
        select_start_pos = 0
    if select_length <= 0:
        select_length = 1
    if select_start_pos + select_length not in range(0, len(all_words)):
        select_length = len(all_words) - select_start_pos
    if select_length < word_num:
        select_length = word_num
    words_to_select = all_words[select_start_pos: select_start_pos + select_length]
    if flag_random:
        shuffle(words_to_select)
    selected_words = words_to_select[0: word_num]
    if book_num <= 0:
        book_num = 1
    #args processing
    for i in range(0, book_num):
        with open(f'./wordbooks/untranslated_wordbook_{book_index + i}.txt', 'w') as f:
            for index_group, word_group in enumerate(selected_words):
                f.write(f'Word Group {index_group + 1}: \n')
                words_in_group = word_group.split(', ')
                for word in words_in_group:
                    f.write(f'{word}\n')
    #untranslated_wordbook generate
    translator = Translate(proxies = {'https': 'socks5://localhost:4781'})
    for i in range(0, book_num):
        with open(f'./wordbooks/translated_wordbook_{book_index + i}.txt', 'w') as f:
            for index_group, word_group in enumerate(selected_words):
                f.write(f'Word Group {index_group + 1}: \n')
                words_in_group = word_group.split(', ')
                for word in words_in_group:
                    f.write(f'{word}: ')
                    word_translated = translator.translate(word, target = 'zh-CN', source = 'en').translatedText
                    if isinstance(word_translated, Null):
                        f.write('Fail to translate.\n')
                    else:
                        f.write(f'{word_translated}\n')
    #translated_wordbook generate

def get_max_index_exist() -> int:
    path_wordbook = Path.cwd() / 'wordbooks'
    if not path_wordbook.exists():
        path_wordbook.mkdir()
    max_index = 0
    for root, dirs, files_in_wordbook in walk(path_wordbook):
        for file in files_in_wordbook:
            if file.endswith('.txt'):
                max_index = max(max_index, max([int(index) for index in findall(r'\d+', file)]))
    return max_index + 1



if __name__ == '__main__':
    generate_wordbook(*input_parse(), get_max_index_exist())
