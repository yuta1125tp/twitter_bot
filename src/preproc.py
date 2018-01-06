#coding:utf-8
"""preprocessings"""

import os
import sys
import configparser
import json
import pickle as pkl

import random

import tqdm

from utils.my_logging import my_get_logger
from load_timeline import load_timeline_user_id

config = configparser.ConfigParser()
config.read('config/common.ini')
sys.path.append(config['python path']['natural-language-preprocessings'])
sys.path.append('C:/Users/yshira/Work/natural-language-preprocessings')
path_to_dump_ma = config['path to dump']['morphological_annalysis']

from preprocessings.ja import tokenizer
from preprocessings.ja import normalization


MAXIMUM_NUM_TEXT_OF_TWITTER_MSG=256

def generate_sentence(mc_table, word_db):
    # Generate Sentence
    # 前の単語1つに注目
    count = 0
    sentence = u""
    # 生成する文章のはじめの2単語はランダムに選ぶ
    """
    for w1,w2 in MCtable.keys():
        #print type(MCtable[(w1,w2)])
        #print MCtable
        #for i in range(len(MCtable[(w1,w2)])):
        #    print MCtable[(w1,w2)][i][0],
    """
    # NGram = len(list(mc_table)[0])
    word_tuple = random.choice(
        [k for k in mc_table.keys() if all([e[1] == 0 for e in mc_table[k]])])

    sentence = u"".join(word_tuple)
    while 1:
        # 直前の2単語をもとにその後ろにくる単語を事例ベースで予測。
        # 事例が複数ある場合はランダムに選ぶ

        # w1,w2に存在しないキーの組み合わせが起きるとエラーで落ちる。
        # 最後のツイートの後に言葉が続かないので、キーがなくなる。
        # キーがない場合はもう一度キーを取り直す。
        # 学習用の文章が十分多かったらそんなことなくなるんだろうけど。。。
        if not word_tuple in mc_table:
            break
            #w1, w2  = random.choice(MCtable.keys())
        next_word = random.choice(mc_table[word_tuple])

        # print next_word
        sentence += next_word[0]
        next_word_att = random.choice([elm[1] for elm in mc_table[word_tuple] if elm[0] == next_word[0]])
        if next_word_att==2:
            break
        if len(sentence) > MAXIMUM_NUM_TEXT_OF_TWITTER_MSG:
            break
        # print(sentence.encode("sjis"))
        word_tuple = tuple(list(word_tuple)[1:] + [next_word[0]])
        count += 1
    return sentence

def make_markov_chain_table(text_ma_list, word_db, NGram=2):
    """
    text_ma_list:分かち済み文字列
    word_db:文字列のリスト"""
    assert NGram > 0, "NGram({}) must be greater than 0".format(NGram)
    # Create table of Markov Chain
    mc_table = {}
    # mc_tableにどんどん事例を保存していく。
    # 事例: (w1, w2) -> (w3, att)
    # キー：直前の2単語w1,w2
    # 値：次につづく単語w3とw1,w2の組の属性att
    # w1,w2,w3 : str : word
    # att : int : 属性 0:文頭, 1:文中, 2:文末
    word_tuple = tuple([u"" for i in range(NGram)])
    for text_ma in text_ma_list:
        # w1 = u""
        # w2 = u""
        att = 0
        for word_idx, word in enumerate(text_ma):
            # idx = word_db.index(word)
            if any(word_tuple):  # u""はFalse扱い
                if word_tuple not in mc_table:
                    mc_table[word_tuple] = []  # 初めて見る単語の連続だった場合はキーに登録
                if word_idx == len(text_ma) - 1:  # 文末の場合
                    att = 2
                mc_table[word_tuple].append((word, att))  # そのキーの後に続く単語を登録(リスト)
                if att == 0:
                    att = 1
            word_tuple = tuple(list(word_tuple)[1:] + [word])  # 次の単語に移る
    return mc_table


def make_word_db(maed_text_list, word_db=set()):
    for maed_text in maed_text_list:
        word_db = word_db.union(set(maed_text))
    return word_db

def remove_any_entities(timeline):
    """remove entities which has any mentions, urls, hashtags or symbols."""
    # timeline = [ elm for elm in timeline if len(elm['entities']['hashtags'])==0]
    # timeline = [ elm for elm in timeline if len(elm['entities']['symbols'])==0]
    # timeline = [ elm for elm in timeline if len(elm['entities']['user_mentions'])==0]
    # timeline = [ elm for elm in timeline if len(elm['entities']['urls'])==0]
    timeline = [ elm for elm in timeline if all([len(e)==0 for e in elm['entities'].values()])]
    return timeline


def main():
    """main func."""
    logger = my_get_logger(__name__, os.path.basename(__file__)+'.log')
    user_id = 87714006
    timeline = load_timeline_user_id(user_id, logger)
    # logger.info(json.dumps(timeline, indent=2, sort_keys=True))

    logger.info('# of elms {}'.format(len(timeline)))
    timeline = remove_any_entities(timeline)
    logger.info('# of elms {}'.format(len(timeline)))

    timeline_text = [elm['text'] for elm in timeline if 'text' in elm]

    t = tokenizer.MeCabTokenizer()    

    timeline_ma = []

    for text in tqdm.tqdm(timeline_text):
        # replace multibyte characters
        text = text.encode("cp932", errors="ignore").decode('cp932')
        logger.debug(f'remove multibytes : {text}')
        words = t.wakati_baseform(text)
        logger.debug(f'baseform          : {words}')
        words = [normalization.normalize(word) for word in words]    
        logger.debug(f'normalized        : {words}')
        timeline_ma.append(words)

    os.makedirs(path_to_dump_ma, exist_ok=True)
    lines=[]
    lines.append(u"{}\n".format(len(timeline_ma)))
    for text_ma in timeline_ma:
        lines.append(u" ".join(text_ma) + u"\n")
    with open(os.path.join(path_to_dump_ma, "tweets_ma.txt"), "wb") as fp:
        fp.writelines([l.encode('utf-8') for l in lines])
    
    word_db = []
    mc_table = make_markov_chain_table(timeline_ma, word_db, NGram=3)
    pkl.dump(mc_table, open(os.path.join(path_to_dump_ma, "mc_table.pkl"), "bw"))

    logger.info(mc_table)

    sentence = generate_sentence(mc_table, word_db)
    logger.info(sentence)


if __name__ == "__main__":
    main()
