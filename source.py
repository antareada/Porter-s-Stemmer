#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nchugueva'

import re
        # Модуль re предоставляет интерфейс для регулярных выражений,
        # что позволяет компилировать регулярные выражения в объекты,
        #а затем выполнять с ними сопоставления.
import codecs

#  Классы окончаний превращаем в регулярные выражения

regexp_start = re.compile(u'[^ая]')
#  Perfective gerund
regexp_perf_gerund1 = re.compile(u'[ая](в|вши|вшись)$')
regexp_perf_gerund2 = re.compile(u'(ив|ивши|ившись|ыв|ывши|ывшись)$')
#  Adjective
regexp_adjective = re.compile(u'(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|ую|юю|ая|яя|ою|ею)$')
#  Participle
regexp_participle1 = re.compile(u'[ая](ем|нн|вш|ющ|щ)$')
regexp_participle2 = re.compile(u'(ивш|ывш|ующ)$')
#  Reflexive
regexp_reflexive = re.compile(u'(ся|сь)$')
#  Verb
regexp_verb1 = re.compile(u'[ая](ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно)$')
regexp_verb2 = re.compile(u'(ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ен|ило|ыло|ено|ят|ует|уют|ит|ыт|ены|ить|ыть|ишь|ую|ю)$')
#  Noun
regexp_noun = re.compile(u'(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я)$')
#  Superlative
regexp_superlative = re.compile(u'(ейш|ейше)$')
#  Derivational
regexp_derivational = re.compile(u'(ост|ость)$')
#  Гласные
regexp_vowels = re.compile(u'[аеиоуыэюя]')

# Регулярка для R1 и R2. Первая гласная, а вторая не гласная.
regexp_rv1 = re.compile(u'([аеиоуыэюя][^аеиоуыэюя])')
regexp_i = re.compile(u'(и)$')
regexp_nn = re.compile(u'(нн)$')
regexp_ = re.compile(u'(ь)$')


# Получаем RV.
# RV - это часть слова после первой гласной,
# или конец слова, если в слове нет гласных.
# Возвращяет: либо номер буквы после гласной, либо конец слова.
def get_rv(word):
    # Регулярка ищет до первого совпадения.
    # Находит первую гласную в слове.
    match = re.search(regexp_vowels, word)

    # Если гласная найдена, то запоминаем номер буквы,
    # которая идет за этой гласной.
    if match:
        id_vowels = match.end()
        rv = word[id_vowels:]  # Получили RV
        print('Это наше rv:\n', rv)  # Отладка.
        return id_vowels
    else:
        return len(word)


# Получаем часть R2. Получается из R1.
# R1 - это часть слова после сочетания "согласная-гласная".
# R2 - это часть R1 после сочетания "согласная-гласная".
# Возвращает либо номер буквы, либо конец слова.
def get_r2(word):
    match = re.search(regexp_rv1, word)
    if match:
        id_vowels = match.end()
        r1 = word[id_vowels:]
        print('Это наше r1:\n', r1)  # отладка
        match = regexp_rv1.search(word, id_vowels)
        if match:
            id_vowels = match.end()
            r2 = r1[id_vowels:]
            print('Это наше r2:\n', r2)  # отладка
            return id_vowels
        else:
            return len(word)
    else:
        return len(word)


def get_stem(word):

    id_rv = get_rv(word)

    # Получаем R2
    id_rv2 = get_r2(word)

    # Ищем окончание Perfective gerund.
    stem_perf_gerund1 = regexp_perf_gerund1.search(word, id_rv)
    stem_perf_gerund2 = regexp_perf_gerund2.search(word, id_rv)

    # Ищем окончание Reflexive.
    stem_reflexive = regexp_reflexive.search(word, id_rv)


    stem_start = regexp_start.search(word, id_rv)

    # match, word = search(word, stem_perf_gerund1, id_rv)
    # if match:
    #     ...

    # Ищем окончание Perfective gerund. Если есть - убираем и завершаем этот шаг.
    # Если нет - пробуем убрать Reflexive.
    if stem_perf_gerund1:
        word = word[:stem_perf_gerund1.start() + (word[stem_perf_gerund1.start()] in (u"а", u"я"))]
        print('Слово после обрезки (stem_perf_gerund2):\n', word)  # отладка
    elif stem_perf_gerund2:
        word = word[:stem_perf_gerund2.start()]
        print('Слово после обрезки (stem_regexp_participle2):\n', word)  # отладка
    else:
        if stem_reflexive:
            word = word[:stem_reflexive.start()]
            print('Слово после обрезки (stem_reflexive):\n', word) # отладка

        stem_adjective = regexp_adjective.search(word, id_rv)
        stem_verb1 = regexp_verb1.search(word, id_rv)
        stem_verb2 = regexp_verb2.search(word, id_rv)
        stem_noun = regexp_noun.search(word, id_rv)
        if stem_adjective:
            word = word[:stem_adjective.start()]
            stem_participle1 = regexp_participle1.search(word, id_rv)
            stem_participle2 = regexp_participle2.search(word, id_rv)
            if stem_participle1:
                word = word[:stem_participle1.start() + (word[stem_participle1.start()] in (u"а", u"я"))]
            elif stem_participle2:
                word = word[:stem_participle2.start()]
            print('Слово после обрезки (stem_adjective):\n', word)  # отладка
        elif stem_verb1:
                word = word[:stem_verb1.start() + (word[stem_verb1.start()] in (u"а", u"я"))]
                print('Слово после обрезки (stem_verb1):\n', word)  # отладка
        elif stem_verb2:
            word = word[:stem_verb2.start()]
            print('Слово после обрезки (stem_verb2):\n', word)  # отладка
        elif stem_noun:
            word = word[:stem_noun.start()]
            print('Слово после обрезки (stem_noun):\n', word, stem_noun.start(), stem_noun.group())  # отладка

    # Пункт 2
    stem_i = regexp_i.search(word, id_rv)
    if stem_i:
        word = word[:stem_i.start()]
        print('Слово после обрезки (stem_i):\n', word)  # отладка

    # Пункт 3
    stem_derivational = regexp_derivational.search(word, id_rv2)
    if stem_derivational:
        word = word[:stem_derivational.start()]
        print('Слово после обрезки (stem_derivational):\n', word)  # отладка

    # Пункт 4
    stem_nn = regexp_nn.search(word, id_rv)
    stem_superlative = regexp_superlative.search(word, id_rv)
    stem_ = regexp_.search(word, id_rv)
    if stem_nn:
        word = word[:stem_nn.start()] + u'н'
        print('Слово после обрезки (stem_nn):\n', word)  # отладка
    elif stem_superlative:
        word = word[:stem_superlative.start()]
        stem_nn = regexp_nn.search(word, id_rv)
        if stem_nn:
            word = word[:stem_nn.start()] + u'н'
            print('Слово после обрезки (stem_nn после stem_superlative):\n', word)  # отладка
        else:
            print('Слово после обрезки (stem_superlative):\n', word)  # отладка
    elif stem_:
        word = word[:stem_.start()]
        print('Слово после обрезки (stem_):\n', word)  # отладка

    return word


def search(word, reg, id):
    stem = reg.search(word, id)
    if stem:
        return True, word[:stem.start()]
    else:
        return False, word


def test_reg(regexp, word, expected):
    reg = regexp.sub('', word)
    print(reg)
    if reg != expected:
        print(u'false')


#with codecs.open("diffs.txt", 'rb', encoding='utf-8') as myFile:  # конструкция гарантирует закрытие
#    for line in myFile:
#        word, expected_stem = line.split()
#        actual_stem = get_stem(word)
#        if actual_stem != expected_stem:
#            print "word:", word, " expected:", expected_stem, " actual:", actual_stem
#            break
#    else:
#        print "ololo congrats"

get_stem(u'противоестественном')