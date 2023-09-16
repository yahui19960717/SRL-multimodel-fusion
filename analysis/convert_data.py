'''
将数据BES转换成BII， BE， BIES
谓词从1开始计算,论元也是
'''
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

def write_data(sentences, outfile):
    with open(outfile, "w", encoding="utf-8") as f_out:
        for i in sentences:
            print(i)
            exit()

def insert_predicate(sentences):
    new_s = []   
    for words, lemma, pos, labels, pred, args in sentences:
        for p in pred:
            if len(args[0][p]) != 0:
                for i in range(len(args[0][p])):
                    if p < args[0][p][i][0]:
                        args[0][p].insert(i, [p,p,"0:[prd]"])
                        break
            else:
                print("异常！不能确保谓词都是有论元的！")
                exit()
            # print(args[0][p])
        new_s.append([words, lemma, pos, labels, pred, args])

    return new_s


def get_sentences_preds(orginal):
    print(orginal,":")
    sentences = read_data(orginal)
    pred_num, true_pred_num = 0, 0
    new_s = []
    for words, lemma, pos, labels in sentences: 
        # 遍历每个句子
        pred, args = [], []
        # 找谓词 print(words, labels)
        for i in range(len(labels)):
            if labels[i] != "_":
                if "|" not in labels[i]:
                    if labels[i] ==  "0:[prd]":
                        pred.append(i+1)
                else:
                    temp = labels[i].split("|")
                    for t in temp :
                        if t == "0:[prd]":
                            pred.append(i+1)
        # 每个句子中的谓词
        if len(pred) == 0:
            pred_num += 1
        else:
            pred_num += len(pred)
        true_pred_num += len(pred)
        
        # 找每个谓词的论元
        flag, dic_p = 0, {} # 标记是否为B
        for p in pred:
            dic_p[p], begin = [],0
            for i in range(len(labels)):
                if labels[i] != "_":
                    if "|" not in labels[i]:
                        if int(labels[i].split(":")[0]) == p:
                            if labels[i].split(":")[1].split("-")[0] == "S":
                                role = "-".join(labels[i].split(":")[1].split("-")[1:])
                                dic_p[p].append([i+1, i+1, role])
                            elif labels[i].split(":")[1].split("-")[0] == "B":
                                flag = 1
                                begin = i+1
                                role = "-".join(labels[i].split(":")[1].split("-")[1:])
                            elif labels[i].split(":")[1].split("-")[0] == "E":
                                flag = 0
                                # print("-".join(labels[i].split(":")[1].split("-")[1:]))
                                dic_p[p].append([begin, i+1, role])        
                        # print(labels[i].split(":")[0], labels[i].split(":")[1])
                    else:
                        temp = labels[i].split("|")
                        for t in temp :
                            if int(t.split(":")[0]) == p:
                                if t.split(":")[1].split("-")[0] == "S":
                                    role = "-".join(t.split(":")[1].split("-")[1:])
                                    dic_p[p].append([i+1, i+1, role])
                                elif t.split(":")[1].split("-")[0] == "B":
                                    flag = 1
                                    begin = i+1
                                    role = "-".join(t.split(":")[1].split("-")[1:])
                                elif t.split(":")[1].split("-")[0] == "E":
                                    flag = 0
                                    # print("-".join(labels[i].split(":")[1].split("-")[1:]))
                                    dic_p[p].append([begin, i+1, role])                                 
        args.append(dic_p) 
        new_s.append([words, lemma, pos, labels, pred, args])
    print("all number of predicate:(没有谓词的句子算一个谓词)",pred_num)
    print("predicted number :(不算没有谓词的句子)", true_pred_num)
    print(len(new_s))
    
    new_s = insert_predicate(new_s)
    return new_s

    

def toBII(orginal, outfile):
    out = open(outfile, "w", encoding="utf-8")
    sentences = get_sentences_preds(orginal)
    for words, lemma, pos, labels, pred, args in sentences:
        if len(pred) == 0:
            for i in range(len(words)):
                # print(words[i], i+1)
                out.write("\t".join([str(i+1), words[i], lemma[i], "_", pos[i], "_", "_", "_", "_", "_"]))
                out.write("\n")
            out.write("\n")
        else:
            for i in range(len(words)):
                srl_label = []
                for p in pred:
                    all_spans = args[0][p]
                    for span in all_spans:
                        if i+1 == span[0]:
                            if span[2] == "0:[prd]":
                                srl_label.append(span[2])
                            else:
                                srl_label.append(str(p)+":B-"+span[2])
                        elif i+1 < span[0]:
                            break
                        elif  span[0]<i+1<=span[1]:
                            srl_label.append(str(p)+":I-"+span[2])

                if len(srl_label) == 1:
                    out.write("\t".join([str(i+1), words[i], lemma[i], "_", pos[i], "_", "_", "_", srl_label[0], "_"]))
                    out.write("\n")
                elif len(srl_label) == 0:
                    out.write("\t".join([str(i+1), words[i], lemma[i], "_", pos[i], "_", "_", "_", "_", "_"]))
                    out.write("\n")
                else: 
                    out.write("\t".join([str(i+1), words[i], lemma[i], "_", pos[i], "_", "_", "_", "|".join(srl_label), "_"]))
                    out.write("\n")
            out.write("\n")
            # for i in pred:
            # exit()
    out.close()

def toBE(orignal, outfile):
    out = open(outfile, "w", encoding="utf-8")
    sentences = get_sentences_preds(orignal)
    for words, lemma, pos, labels, pred, args in sentences:
        if len(pred) == 0:
            for i in range(len(words)):
                out.write("\t".join([str(i+1), words[i], lemma[i], "_", pos[i], "_", "_", "_", "_", "_"]))
                out.write("\n")
            out.write("\n")
        else:
            for i in range(len(words)):
                srl_label = []
                for p in pred:
                    all_spans = args[0][p]
                    for span in all_spans:
                        if i+1 == span[0]:
                            if span[2] == "0:[prd]":
                                srl_label.append(span[2])
                            else:
                                srl_label.append(str(p)+":B-"+span[2])
                        elif i+1 < span[0]:
                            break
                        elif  i+1==span[1]:
                            srl_label.append(str(p)+":E-"+span[2])
                if len(srl_label) == 1:
                    out.write("\t".join([str(i+1), words[i], lemma[i], "_", pos[i], "_", "_", "_", srl_label[0], "_"]))
                    out.write("\n")
                elif len(srl_label) == 0:
                    out.write("\t".join([str(i+1), words[i], lemma[i], "_", pos[i], "_", "_", "_", "_", "_"]))
                    out.write("\n")
                else: 
                    out.write("\t".join([str(i+1), words[i], lemma[i], "_", pos[i], "_", "_", "_", "|".join(srl_label), "_"]))
                    out.write("\n")
            out.write("\n")
    out.close()

def toBIES(original, outfile):
    out = open(outfile, "w", encoding="utf-8")
    sentences = get_sentences_preds(original)
    for words, lemma, pos, labels, pred, args in sentences:
        if len(pred) == 0:
            for i in range(len(words)):
                out.write("\t".join([str(i+1), words[i], lemma[i], "_", pos[i], "_", "_", "_", "_", "_"]))
                out.write("\n")
            out.write("\n")
        else:
            for i in range(len(words)):
                srl_label = []
                for p in pred:
                    all_spans = args[0][p]
                    for span in all_spans:
                        if (i+1) == span[0] and (i+1) == span[1]:
                            if span[2] == "0:[prd]":
                                srl_label.append(span[2])
                            else:
                                srl_label.append(str(p)+":S-"+span[2])
                        elif (i+1) == span[0] and (i+1) != span[1]:
                            srl_label.append(str(p)+":B-"+span[2])
                        elif (i+1) < span[0]:
                            break
                        elif span[0] < (i+1) < span[1]:
                            srl_label.append(str(p)+":I-"+span[2])
                        elif  (i+1) != span[0] and (i+1)==span[1]:
                            srl_label.append(str(p)+":E-"+span[2])
                        # elif span[1]<(i+1):
                        #     break
                if len(srl_label) == 1:
                    out.write("\t".join([str(i+1), words[i], lemma[i], "_", pos[i], "_", "_", "_", srl_label[0], "_"]))
                    out.write("\n")
                elif len(srl_label) == 0:
                    out.write("\t".join([str(i+1), words[i], lemma[i], "_", pos[i], "_", "_", "_", "_", "_"]))
                    out.write("\n")
                else: 
                    out.write("\t".join([str(i+1), words[i], lemma[i], "_", pos[i], "_", "_", "_", "|".join(srl_label), "_"]))
                    out.write("\n")
            out.write("\n")
    out.close()

def sl_toBII(BIES_f, BII_f) :
    with open(BIES_f, "r", encoding="utf-8") as f, open(BII_f, "w", encoding="utf-8") as f_out:
        for line in f:
            if len(line.strip())==0:
                f_out.write(line)
            else:
                line_new = line.strip().split("\t")
                if line.strip().split("\t")[8] == "_" or line.strip().split("\t")[8] == "0:[prd]":
                    f_out.write(line)
                else:

                    if len(line.strip().split("\t")[8].split("|")) == 1:
                        # 只有一个标签
                        p_labels = line.strip().split("\t")[8].split(":")
                        temp = p_labels[1].split("-")
                        if temp[0] == "E":
                            p_labels[1] = "".join(["I-", "-".join(temp[1:])])
                            line_new[8] = ":".join(p_labels)
                            f_out.write("\t".join(line_new)+"\n")
                        elif temp[0] == "S":
                            p_labels[1] = "".join(["B-", "-".join(temp[1:])])
                            line_new[8] = ":".join(p_labels)
                            f_out.write("\t".join(line_new)+"\n")
                        else:
                            f_out.write(line)
                    else:
                        # 有多个标签
                        temp_labels = []
                        labels = line.strip().split("\t")[8].split("|")
                        for label in labels:
                            p_labels = label.split(":")
                            temp=p_labels[1].split("-")
                            if temp[0] == "E":
                                p_labels[1]="".join(["I-", "-".join(temp[1:])])
                                temp_labels.append(":".join(p_labels))
                            elif temp[0] == "S":
                                p_labels[1]="".join(["B-", "-".join(temp[1:])])
                                temp_labels.append(":".join(p_labels))
                            else:
                                temp_labels.append(":".join(p_labels))
                        line_new[8]="|".join(temp_labels)
                        f_out.write("\t".join(line_new)+"\n")


if __name__=="__main__":
    # single
    BES_train = "../data/BES/conll05/BES-train.conllu"
    BES_dev = "../data/BES/conll05/BES-dev.conllu"
    BES_test = "../data/BES/conll05/BES-wsj.conllu"
    bes_debug = "../data/BES/conll05/debug.conllu"
    singl_BES_train = "../data/BES/conll05/BES-train-single.conllu"
    singl_BES_dev = "../data/BES/conll05/BES-dev-single.conllu"
    singl_BES_test = "../data/BES/conll05/BES-wsj.conllu"

    BII_train = "../data/BII/conll05/BII-train.conllu"
    BII_dev   = "../data/BII/conll05/BII-dev.conllu"
    BII_test  = "../data/BII/conll05/BII-wsj.conllu"

    BE_train = "../data/BE/conll05/BE-train.conllu"
    BE_dev   = "../data/BE/conll05/BE-dev.conllu"
    BE_test  = "../data/BE/conll05/BE-wsj.conllu"


    BIES_train = "../data/BIES/conll05/BIES-train.conllu"
    BIES_dev   = "../data/BIES/conll05/BIES-dev.conllu"
    BIES_test  = "../data/BIES/conll05/BIES-wsj.conllu"

    sl_BIES_train  = "../data/BIES-conll05/BIES-train.conllu"
    sl_BIES_dev = "../data/BIES-conll05/BIES-dev.conllu"
    sl_BIES_wsj = "../data/BIES-conll05/BIES-wsj.conllu"
    sl_BIES_brown = "../data/BIES-conll05/BIES-brown.conllu"

    sl_BII_train = "../data/BII-conll05/BII-train.conllu"
    sl_BII_dev = "../data/BII-conll05/BII-dev.conllu"
    sl_BII_wsj = "../data/BII-conll05/BII-wsj.conllu"
    sl_BII_brown = "../data/BII-conll05/BII-brown.conllu"

    sl_toBII(sl_BIES_train, sl_BII_train)
    sl_toBII(sl_BIES_dev, sl_BII_dev)
    sl_toBII(sl_BIES_wsj, sl_BII_wsj)
    sl_toBII(sl_BIES_brown, sl_BII_brown)
    exit()
    # toBIES(bes_debug, BIES_test)
    # exit()
    toBIES(BES_train, BIES_train)
    toBIES(BES_dev, BIES_dev)
    toBIES(BES_test, BIES_test)

    toBII(BES_test, BII_test)
    toBII(BES_dev, BII_dev)
    toBII(BES_train, BII_train)


    toBE(BES_train, BE_train)
    toBE(BES_dev, BE_dev)
    toBE(BES_test, BE_test)


    