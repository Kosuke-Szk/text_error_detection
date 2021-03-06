import MeCab
import random
import pprint

try:
	tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd -Ochasen')
except:
	tagger = MeCab.Tagger('-Ochasen')
tagger.parse('')

def process(text, exclude_rate=0.5, include_rate=0.5, repeat_rate=0.1, delete_rate=0.1):
	res = []
	text1 = random_exclude_RA(text, exclude_rate)
	text2 = random_include_SA(text, include_rate)
	text3 = random_repeat_END(text, repeat_rate)
	text4 = random_delete_MID(text, delete_rate)
	for t1, t2, t3, t4 in zip(text1, text2, text3, text4):
		txt = []
		for w1, w2, w3, w4 in zip(t1, t2, t3, t4):
			count_dict = dict()
			for w in [w1, w2, w3, w4]:
				count_dict.setdefault(w, 1)
				count_dict[w] += 1
			min_w = min(count_dict, key=count_dict.get) # 最も珍しい単語を追加
			txt.append(min_w)
		res.append(txt)
	return [''.join(row) for row in res]

def random_exclude_RA(text, exclude_rate):
    res = []
    for sentence in text:
        parsed_sen = []
        node = tagger.parseToNode(sentence)
        while node:
            if node.feature.split(',')[-3] == 'られる' and node.feature.split(',')[1] == '接尾':
                if random.random() < exclude_rate:
                    parsed_sen.append('れる')
                else:
                    parsed_sen.append(node.surface)                    
            else:
                parsed_sen.append(node.surface)
            node = node.next
        # res.append(''.join(parsed_sen))
        res.append(parsed_sen)
    return res

def random_include_SA(text, include_rate):
    res = []
    for sentence in text:
        parsed_sen = []
        node = tagger.parseToNode(sentence)
        prior_cond = False
        while node:
            if prior_cond: # 前の単語が五段活用未然形だった場合
                if node.feature.split(',')[1] == '接尾' and node.feature.split(',')[-3] == 'せる':
                    if random.random() < include_rate:
                        parsed_sen.append('させ')
                    else:
                        parsed_sen.append(node.surface)
                prior_cond = False
            elif ('五段' in node.feature.split(',')[4]) and ('サ行' not in node.feature.split(',')[4]) and node.feature.split(',')[-4] == '未然形':
                prior_cond = True # 語段活用未然形の動詞がきたら構える
                parsed_sen.append(node.surface)
            else:
                parsed_sen.append(node.surface)
            node = node.next
        # res.append(''.join(parsed_sen))
        res.append(parsed_sen)
    return res

def random_repeat_END(text, repeat_rate):
    res = []
    for sentence in text:
        parsed_sen = []
        node = tagger.parseToNode(sentence)
        while node:
            if is_hiragana(node.surface) and node.surface != '': # ひらがなの場合のみ語尾をリピートする
                if random.random() < repeat_rate:
                    parsed_sen.append(str(node.surface) + str(node.surface[-1]))
                else:
                    parsed_sen.append(node.surface)
            else:
                parsed_sen.append(node.surface)
            node = node.next
        # res.append(''.join(parsed_sen))
        res.append(parsed_sen)
    return res

def random_delete_MID(text, delete_rate):
    res = []
    for sentence in text:
        parsed_sen = []
        node = tagger.parseToNode(sentence)
        while node:
            if is_hiragana(node.surface) and node.surface != '': # ひらがなの場合のみ中間文字をdropする
                if random.random() < delete_rate:
                    k = random.choice(range(len(node.surface)))
                    parsed_sen.append(''.join([c for i, c in enumerate(node.surface) if i != k]))
                else:
                    parsed_sen.append(node.surface)
            else:
                parsed_sen.append(node.surface)
            node = node.next
        # res.append(''.join(parsed_sen))
        res.append(parsed_sen)
    return res

def is_hiragana(title):
    a =   [ch for ch in title if "ぁ" <= ch <= "ん"]
    if len(title) == len(a):
        return True
    return False

def is_katakana(title):
    a =   [ch for ch in title if "ァ" <= ch <= "ン"]
    if len(title) == len(a):
        return True
    return False

if __name__ == '__main__':
	text = [
		'それでは、ただいまより歌わせていただきます',
		'重要な予定があるので明日は起きられる',
		'ここからは富士山を見られる',
		'それでは、ただいまより話させていただきます'
	]
	res = process(text)
	print('Raw text as below')
	pprint.pprint(text)
	print()
	print('Broken text as below')
	pprint.pprint(res)