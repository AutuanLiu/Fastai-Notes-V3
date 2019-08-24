import jieba
import pkuseg

from gensim.models import word2vec
# 引入日志配置
import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def preprocess_in_the_name_of_people_jieba():
    # 分词效果太差
    with open("in_the_name_of_people.txt", mode='rb') as f:
        doc = f.read()
        doc_cut = jieba.cut(doc)
        result = ' '.join(doc_cut)
        result = result.encode('utf-8')
        with open("in_the_name_of_people_cut_jieba.txt", mode='wb') as f2:
            f2.write(result)


def preprocess_in_the_name_of_people_pku():
    pkuseg.test("in_the_name_of_people.txt", "in_the_name_of_people_cut.txt", nthread=2)


def train_in_the_name_of_people():
    sent = word2vec.Text8Corpus(fname="in_the_name_of_people_cut.txt")
    model = word2vec.Word2Vec(sentences=sent)
    model.save("in_the_name_of_people.model")


def train_line_sentence():
    with open("in_the_name_of_people_cut.txt", mode='rb') as f:
        # 传递open的fd
        sent = word2vec.LineSentence(f)
        model = word2vec.Word2Vec(sentences=sent)
        model.save("line_sentnce.model")


def train_PathLineSentences():
    # 传递目录，遍历目录下的所有文件
    sent = word2vec.PathLineSentences("in_the_name_of_people.txt")
    model = word2vec.Word2Vec(sentences=sent)
    model.save("PathLineSentences.model")


def train_left():
    sent = word2vec.Text8Corpus(fname="in_the_name_of_people_cut.txt")
    # 定义模型
    model = word2vec.Word2Vec()
    # 构造词典
    model.build_vocab(sentences=sent)
    # 模型训练
    model.train(sentences=sent, total_examples=model.corpus_count, epochs=model.iter)
    model.save("left.model")


if __name__ == '__main__':
    preprocess_in_the_name_of_people_jieba()
    preprocess_in_the_name_of_people_pku()
    train_in_the_name_of_people()
    train_line_sentence()
    train_PathLineSentences()
    train_left()

    model2 = word2vec.Word2Vec.load("in_the_name_of_people.model")
    print(model2.most_similar("吃饭"))
    print(model2.wv("吃饭"))
