
def read_data(orginal):
    sentences, words, lemma, pos, labels = [], [], [], [], []
    with open(orginal, "r", encoding="utf-8") as f_in:
        for line in f_in:
            if len(line.strip()) == 0:
                sentences.append([words, lemma, pos, labels])
                words, lemma, pos, labels = [], [], [], []
            else:
                words.append(line.strip().split()[1])
                lemma.append(line.strip().split()[2])
                pos.append(line.strip().split()[4])
                labels.append(line.strip().split()[8])
    print("all number of sentences :", len(sentences))   
    return sentences


def compare(f1, f2):
    for i in range(len(f1)):
        if f1[i][0] == f2[i][0]:
            if f1[i][3]== f2[i][3]:
                continue
            else:
                # print(f1[i][0])
                for j in range(len(f1[i][3])):
                    if f1[i][3][j] != f2[i][3][j]:
                        print(f1[i][3][j])
                        print(f2[i][3][j])
                        exit()
                print("不一致，我错了")
                # exit()
        else:
            print("wrong")
            
# BE_me = read_data("../data/BE/conll05/BE-wsj.conllu")
# BE_sl = read_data("../data/BE-conll05/sc-conll5-wsj.conllu")
# compare2(BE_me, BE_sl)
# exit()
BIES_sl = read_data("../data/BIES-conll05/BIES-wsj.conllu")
BIES_me = read_data("../data/BIES/conll05/BIES-wsj.conllu")
compare(BIES_me, BIES_sl)