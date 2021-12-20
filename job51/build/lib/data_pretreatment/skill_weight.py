import csv
import jieba.analyse
import sys

from job51.data_pretreatment.dataClean import connectMysql
from job51.util.file_list import get_file_names


def skill_weight():
    connectMysql("truncate table skw_devops")
    sys.path.append("../")
    # 加载停用词文件
    stopWords = open('../jieba/stopWords.txt', encoding='utf-8').read()
    jieba.del_word('数据分析')
    jieba.del_word('运维')

    wantWords = open('../jieba/wantWords.txt', encoding='utf-8').read()
    # 转换词
    synonymWords = {'自然语言': "Nlp", '人工智能': 'Ai', 'Boot': 'Springboot', 'Node': 'Nodejs','Js':'Javascript','Jq': 'Jquery','Reactjs': 'React'}
    keys = list(synonymWords.keys())
    # 添加不被分词的单词
    jieba.load_userdict("../jieba/customWords.txt")
    file_names = get_file_names()
    for file_name in file_names:
        print(file_name)
        with open('../test_data/'+file_name, 'r', encoding='gbk')as f:
            reader = csv.DictReader(f)
            dataList = [row['position_desc'] for row in reader]
            words_list = []
            final_word_list = []
            for data in dataList:
                wordList = jieba.lcut(data, HMM=False)
                for word in wordList:
                    word = word.strip().capitalize()
                    if word not in stopWords:
                        words_list.append(word)
            for word in words_list:
                if word in keys:
                    word = synonymWords[word]
                    final_word_list.append(word)
                if word in wantWords:
                    final_word_list.append(word)
            final_sentence = ' '.join(final_word_list)
            print("第一次清洗后：\n" + ' '.join(words_list))
            print("=" * 150)
            print("第二次清洗后：\n" + final_sentence)
            print("=" * 150)
            # 实例化TextRank()，设置窗口大小
            text = jieba.analyse.TextRank()
            text.span = 8
            ws = text.textrank(final_sentence, topK=25, withWeight=True, allowPOS=['eng', 'n'])
            # ws = jieba.analyse.extract_tags(final_sentence, topK=20, withWeight=True, allowPOS=['eng', 'n'])
            for w in ws:
                sql = "insert into skw_devops (skill,weight) values {} ".format(w)
                print(sql)
                connectMysql(sql)
        f.close()


if __name__ == '__main__':
    skill_weight()
