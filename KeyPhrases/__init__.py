# -*- coding: utf-8 -*-
import subprocess
import re
from subprocess import call
# from subprocess import Popen, PIPE
from bs4 import BeautifulSoup


# from math import log

def getKeyPhrasesOnly(text):
    kp_dict = getKeyPhrasesDict(text)
    result = []
    for group in kp_dict:
        max_n = int(len(kp_dict[group]) * 0.8) + 1
        counter = 0
        temp = []
        for item in kp_dict[group]:
            if item['frequency'] > 1 and counter < max_n:
                temp += [item['key_phrase']]
                counter += 1
        result += temp
    return result


def getKeyPhrasesDict(text):
    # build .txt file with text
    f = open('./temp/text.txt', 'w')
    f.write(text.encode('utf-8'))
    f.close()
    # run tomita parser

    # call(["./grammar/tomita-linux64", "./grammar/config.proto"], stdout=subprocess.PIPE)
    call(["./grammar/tomitaparser.exe", "./grammar/config.proto"], stdout=subprocess.PIPE)

    tomita_result = open('./temp/result.html').read().replace('</html>', '')
    # bs for parsing
    html = BeautifulSoup(tomita_result, "html.parser")
    # results in <tr><td><a></a></td><td></td></tr> tags
    result_set = html.find_all('tr')[1:]
    group_names = ['сущ', 'сущ_сущ', 'прил_сущ', 'NNP', 'имя']
    keys = [[], [], [], [], []]
    trash = []
    exclude = 'мусор'
    for row in result_set:
        key = row.find('a')
        key = ''.join(key.findAll(text=True))
        group_name = str(row.select('td:nth-of-type(2)'))[1:-1]
        group_name = re.findall(r"\[([\S]+)\]", group_name)[0]
        if exclude not in group_name:
            for group_name_index in range(len(group_names)):
                if group_name == group_names[group_name_index]:
                    keys[group_name_index] += [key.replace('\'', '').replace('\"', '').lower().strip()]
        else:
            trash += [key]
    # brush up keys list
    sw1_file = './stop-words/stop-words_russian_1_ru.txt'
    sw1 = open(sw1_file, 'r')
    sw1 = sw1.read().split()
    # remove stop words and trash
    keys = [[key for key in keys[i] if key not in trash and key not in sw1] for i in range(len(keys))]
    # get unique keys
    unique_keys = [list(set(keys[i])) for i in range(len(keys))]
    # get frequencies
    frequencies = [[keys[i].count(key) for key in unique_keys[i]] for i in range(len(keys))]
    # build data = {group_name : [ {kp : freq}] }
    data = {}
    data_len = len(group_names)
    for group_name_index in range(data_len):
        data[group_names[group_name_index]] = []
        for index in range(len(unique_keys[group_name_index])):
            # TODO: check if areKPequal. function: check(unique_keys, frequencies, group_index, kp_index). go up and check with each
            data[group_names[group_name_index]].append(
                {'key_phrase': unique_keys[group_name_index][index], 'frequency': frequencies[group_name_index][index]})

    # filter
    data_filtered = {}
    for group_name_index in reversed(range(data_len)):
        data_filtered[group_names[group_name_index]] = []
        for item in data[group_names[group_name_index]]:
            equal = hasEqual(item, group_name_index, data_filtered, group_names)
            if equal == 0:
                data_filtered[group_names[group_name_index]].append(item)
            else:
                g_i = equal[1]
                for item_inner in data_filtered[group_names[g_i]]:
                    if equal[0]['key_phrase'] == item_inner['key_phrase']:
                        if g_i == group_name_index:
                            item_inner['frequency'] += equal[3]
                        else:
                            if item_inner['frequency'] < equal[3]:
                                item_inner['frequency'] = equal[3]

    data = data_filtered
    for group_name in data:
        data[group_name] = sorted(data[group_name], key=lambda k: k['frequency'], reverse=True)
    return data


# TODO: Если в одной группе, то складываем частоты. Иначе просто игнорим более короткое
def hasEqual(item, group_name_index, data, group_names):
    for g_i in range(group_name_index, len(data)):
        for i_i in range(len(data[group_names[g_i]])):
            item_to_check = data[group_names[g_i]][i_i]
            if item_to_check['key_phrase'] == item['key_phrase']: continue
            if areKPequal(item['key_phrase'], item['frequency'], item_to_check['key_phrase'],
                          item_to_check['frequency']):
                return [item_to_check, g_i, i_i, item['frequency']]
    return 0


def areKPequal(kp1, freq1, kp2, freq2):
    # freq share
    _share = 0.8
    # init. key_phrase1 - longest kp
    key_phrase1 = kp1
    key_phrase2 = kp2
    key_phrase1_freq = freq1
    key_phrase2_freq = freq2
    kp1_words_len = len(kp1.split(' '));
    kp2_words_len = len(kp2.split(' '))
    if (kp1_words_len < kp2_words_len):
        key_phrase1 = kp2
        key_phrase2 = kp1
        key_phrase1_freq = freq2
        key_phrase2_freq = freq1

    if kp1_words_len == kp2_words_len:
        if len(key_phrase1) < len(key_phrase2):
            key_phrase1 = kp2
            key_phrase2 = kp1
            key_phrase1_freq = freq2
            key_phrase2_freq = freq1
        if len(key_phrase1) == len(key_phrase2) and key_phrase2_freq < key_phrase1_freq:
            key_phrase1 = kp2
            key_phrase2 = kp1
            key_phrase1_freq = freq2
            key_phrase2_freq = freq1

    # if frequencies are not significant
    if (key_phrase1_freq / float(key_phrase2_freq) < _share): return False
    # check if kp1 contains kp2
    if (not isP1ContainsP2(key_phrase1, key_phrase2)): return False
    return True


def isP1ContainsP2(phrase1, phrase2):
    # word bigrams
    _share = 0.85
    phrase1_word = phrase1.replace(' ', '')
    phrase2_word = phrase2.replace(' ', '')

    phrase1_word_bigramms = getBigramms(phrase1_word)
    phrase2_word_bigramms = getBigramms(phrase2_word)

    p2inp1_counter = 0
    for i_2 in range(len(phrase1_word_bigramms)):
        counter_temp = countEqualBigramms(phrase1_word_bigramms, phrase2_word_bigramms, i_2)
        if (counter_temp > p2inp1_counter): p2inp1_counter = counter_temp

    return p2inp1_counter / float(len(phrase1_word_bigramms)) >= _share


def getBigramms(word):
    result = []
    word_length = len(word)
    for symbol_i in range(word_length):
        if (symbol_i < word_length - 1):
            result += [word[symbol_i:symbol_i + 2]]
    return result


def countEqualBigramms(bigramms1, bigramms2, i_1):
    res = 0
    i_2 = 0
    while (i_2 < len(bigramms2) and i_1 < len(bigramms1)):
        if (bigramms1[i_1] == bigramms2[i_2]):
            res += 1
        i_1 += 1
        i_2 += 1
    return res


def printKP(data):
    for group_name in data:
        print('\n' + group_name)
        counter = 0
        counter_max = 20
        for item in data[group_name]:
            if (item['frequency'] > 1 and counter < counter_max):
                counter += 1
                print(item['key_phrase'] + ' : ' + str(item['frequency']))
