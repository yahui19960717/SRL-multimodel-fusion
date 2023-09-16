# -*-coding:utf-8-*-
import random
from config import config
'''
Note： 
原语料库中第三列的词是lemma形式 原型；
conll05test数据集wjs里面有三个句子重复的
TODO：统计一下标签，哪些标签容易多标注，哪些标签容易错标注，哪些标签容易
'''
def get_orig_sen(file):
    # 获得原始的数据，统计词数和句子数
    with open(file, encoding="UTF-8") as f:
        # 第二行是lemma 原型
        word_num, rel_num = 0, 0
        sentences, words, relations, dic = [], [], [], {}
        for line in f:
            temp = line.strip().split("\t")
            if len(temp) == 1:
                sentences.append([words, relations])
                word_num += len(words)
                rel_num += len(relations)
                if " ".join(words) not in dic.keys():
                    dic[" ".join(words)] = [words, relations]
                else:
                    print(words)
                words, relations = [], []
            else:
                words.append(temp[1])
                relations.append(temp[8])
        print(f"词的个数有：{word_num}")
        print(f"标签的总数有：{rel_num}")
        print(f"总的句子数：{len(sentences)},其中有{len(sentences)-len(dic)} 的句子重复，剩余{len(dic)}个不重复句子。")

    return sentences, dic

def compare_right_rel(s_gold, s_pred):
    # 获得预测和gold不同的标注,每个key是句子
    all, same, no_pre, not_gold, diff, all_diff = 0, 0, 0, 0, 0, 0
    dic_not_pred, dic_not_gold, dic_diff, = {}, {}, {}
    for i in s_gold.keys():
        if i in s_pred.keys():
            for j in range(len(s_pred[i][1])):
                print(s_pred[i][1])
                exit()
                all += 1
                if s_pred[i][1][j] == s_gold[i][1][j]:# 包含-和标注的情况,相同情况
                    same += 1                   
                else:
                    # 预测没有情况
                    all_diff += 1
                    if s_pred[i][1][j] == "_" and s_gold[i][1][j] != "_": # 需要预测但没有预测到的论元
                        no_pre += 1
                        # 存在词典里
                        if i not in dic_not_pred.keys():
                            dic_not_pred[i]=[]
                            dic_not_pred[i].append([j, s_gold[i][0][j], s_gold[i][1][j], "_"])
                        else:
                            dic_not_pred[i].append([j, s_gold[i][0][j], s_gold[i][1][j], "_"])
                    elif s_pred[i][1][j] != "_" and s_gold[i][1][j] == "_": # 不需要预测的论元（多预测的论元）
                        not_gold += 1
                        # 存在词典里
                        if i not in dic_not_gold.keys():
                            dic_not_gold[i]=[]
                            dic_not_gold[i].append([j, s_gold[i][0][j], "_", s_pred[i][1][j]])
                        else:
                            dic_not_gold[i].append([j, s_gold[i][0][j], "_", s_pred[i][1][j]])
                    elif s_pred[i][1][j] != "_" and s_gold[i][1][j] != "_": # 需要预测，但预测错误的论元
                        diff += 1
                        # 存在词典里
                        if i not in dic_diff.keys():
                            dic_diff[i]=[]
                            dic_diff[i].append([j, s_gold[i][0][j], s_gold[i][1][j], s_pred[i][1][j]])
                        else:
                            dic_diff[i].append([j, s_gold[i][0][j], s_gold[i][1][j], s_pred[i][1][j]])
                        
        else:
            print("error! dismatch between training and predict!")
    print(f"标注的词的个数有：{all}")
    print(f"标签不相同的词的个数：{all_diff}")
    print(f"需要预测但没有预测到的结果个数：{not_gold}个, {len(dic_not_gold)}句；")
    print(f"不需要预测但多预测的结果个数：{no_pre}个,{len(dic_not_pred)}句；")
    print(f"在需要预测的结果中，预测错误的结果个数：{diff}个, {len(dic_diff)}句；")
    return dic_not_gold, dic_not_pred, dic_diff

def get_dic_gold(not_pred_dic, not_gold_dic, diff_dic, gold_dic, pred_dic, file):
    f1 = open(file, "w", encoding="utf-8")
    num = 0
    extra_s_dic = {}
    for i in not_pred_dic.keys():
        if i not in extra_s_dic.keys(): # 如果没有预测到论元的句子做过了，预测多论元的句子就不再做了
            extra_s_dic[i] = 0
        extra_not_pred_rel, extra_not_gold_rel, extra_diff_gold, extra_diff_pred= [], [], [], [] # 预测没预测到的论元, 预测多的论元, 两者标注不同的论元
        # note:每个词典里的value元素都是[index，词, gold_label, predict_label]
        for e in not_pred_dic[i]:
            extra_not_pred_rel.append(e[2])
        if i in not_gold_dic.keys(): # 如果是多预测论元的句子
            for e in not_gold_dic[i]:
                extra_not_gold_rel.append(e[3])
        if i in diff_dic.keys():# 如果也是存在预测和gold不同的论元的句子
            for e in dic_diff[i]:
                extra_diff_gold.append(e[2])
                extra_diff_pred.append(e[3])
        if len(i.split()) <= 10:
            # overleaf框架前半部分
            f1.write("\\begin{figure}[htbp]\n\\begin{center}\n\\begin{dependency}[arc edge, arc angle=80, text only label, label style={above}]\n\\begin{deptext} [row sep=0.2cm, column sep=.5cm]\n")
            f1.write("\\&Root\\&"+"\\&".join(i.split())+r'\\'+"\n")
            f1.write("\\end{deptext}\n")

            print("\\begin{figure}[htbp]\n\\begin{center}\n\\begin{dependency}[arc edge, arc angle=80, text only label, label style={above}]\n\\begin{deptext} [row sep=0.2cm, column sep=.5cm]\n")
            # 输出句子
            print("\\&Root\\&"+"\\&".join(i.split())+r'\\'+"\n")
            print("\\end{deptext}\n")
            # note overleaf里面 root的下标从2开始,上面的标注是gold，下面的标注是predict
            if i in gold_dic.keys(): # 输出gold的标注
                rels = []
                for j in range(len(gold_dic[i][1])):
                    if gold_dic[i][1][j] != "_":
                        index_r = gold_dic[i][1][j].split(":")
                        # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                        rels.append([index_r[0], j, index_r[1], gold_dic[i][1][j]]) # 头 尾 标签 头:标签;
                for r in rels:
                    # gold里面需要加2，因为从1开始，j是从0开始，需要加3
                    if r[3] in extra_not_pred_rel:
                        f1.write("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}"+"\n")
                        print("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}")
                    # elif r[3] in extra_not_gold_rel:
                    #     f1.write("\\depedge[edge style={blue,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}"+"\n")
                    #     print("\\depedge[edge style={blue,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}")   
                    elif r[3] in extra_diff_gold:
                        f1.write("\\depedge[edge style={red,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}"+"\n")
                        print("\\depedge[edge style={red,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}")   
                    else:
                        f1.write("\\depedge[edge style={black,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}"+"\n")
                        print("\\depedge[edge style={black,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}")
            if i in pred_dic.keys(): # 输出预测的标注
                rels = []
                for j in range(len(pred_dic[i][1])):
                    if pred_dic[i][1][j] != "_":
                        index_r = pred_dic[i][1][j].split(":")
                        # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                        rels.append([index_r[0], j, index_r[1], pred_dic[i][1][j]]) # 头 尾 标签 头:标签;
                for r in rels:
                    # gold里面需要加2，因为从1开始，j是从0开始，需要加3
                    # if r[3] in extra_not_pred_rel:
                    #     f1.write("\\depedge[edge style={red!40,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}"+"\n")
                    #     print("\\depedge[edge style={red!40,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}")
                    if r[3] in extra_not_gold_rel:
                        f1.write("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}"+"\n")
                        print("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}")   
                    elif r[3] in extra_diff_pred:
                        f1.write("\\depedge[edge style={red,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}"+"\n")
                        print("\\depedge[edge style={red,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}")   
                    else:
                        f1.write("\\depedge[edge style={black,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}"+"\n")
                        print("\\depedge[edge style={black,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}")
            num+=1
            f1.write("\\end{dependency}\n\\label{fig:dang-zuo-fenci}\n\\end{center}\n\\end{figure}\n")
            f1.write("\n")
            print("\\end{dependency}\n\\label{fig:dang-zuo-fenci}\n\\end{center}\n\\end{figure}\n")
            print("\n")
    
    f1.write("--------------------分割线1------------------------\n\n")
    for i in not_gold_dic.keys():
        if i not in extra_s_dic.keys(): # 如果没有预测到论元的句子做过了，预测多论元的句子就不再做了
            extra_s_dic[i] = 0 # 加进去，看只有论元不同的句子去做
            extra_not_pred_rel, extra_not_gold_rel, extra_diff_gold, extra_diff_pred = [], [], [], [] # 预测没预测到的论元, 预测多的论元, 两者标注不同的论元
            for e in not_gold_dic[i]:
                extra_not_gold_rel.append(e[3])
            if i in not_pred_dic.keys(): # 如果是多预测论元的句子
                for e in not_pred_dic[i]:
                    extra_not_pred_rel.append(e[2])
            if i in diff_dic.keys():# 如果也是存在预测和gold不同的论元的句子
                for e in dic_diff[i]:
                    extra_diff_gold.append(e[2])
                    extra_diff_pred.append(e[3])
            if len(i.split()) <= 10:
                # overleaf框架前半部分
                f1.write("\\begin{figure}[htbp]\n\\begin{center}\n\\begin{dependency}[arc edge, arc angle=80, text only label, label style={above}]\n\\begin{deptext} [row sep=0.2cm, column sep=.5cm]\n")
                f1.write("\\&Root\\&"+"\\&".join(i.split())+r'\\'+"\n")
                f1.write("\\end{deptext}\n")

                print("\\begin{figure}[htbp]\n\\begin{center}\n\\begin{dependency}[arc edge, arc angle=80, text only label, label style={above}]\n\\begin{deptext} [row sep=0.2cm, column sep=.5cm]\n")
                # 输出句子
                print("\\&Root\\&"+"\\&".join(i.split())+r'\\'+"\n")
                print("\\end{deptext}\n")
                # note overleaf里面 root的下标从2开始,上面的标注是gold，下面的标注是predict
                if i in gold_dic.keys(): # 输出gold的标注
                    rels = []
                    for j in range(len(gold_dic[i][1])):
                        if gold_dic[i][1][j] != "_":
                            index_r = gold_dic[i][1][j].split(":")
                            # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                            rels.append([index_r[0],j, index_r[1], gold_dic[i][1][j]]) # 头 尾 标签 头:标签;
                    for r in rels:
                        # gold里面需要加2，因为从1开始，j是从0开始，需要加3
                        if r[3] in extra_not_pred_rel:
                            f1.write("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}")
                        # elif r[3] in extra_not_gold_rel:
                        #     f1.write("\\depedge[edge style={blue,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}"+"\n")
                        #     print("\\depedge[edge style={blue,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}")   
                        elif r[3] in extra_diff_gold:
                            f1.write("\\depedge[edge style={red,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={red,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}")   
                        else:
                            f1.write("\\depedge[edge style={black,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={black,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}")
                if i in pred_dic.keys(): # 输出预测的标注
                    rels = []
                    for j in range(len(pred_dic[i][1])):
                        if pred_dic[i][1][j] != "_":
                            index_r = pred_dic[i][1][j].split(":")
                            # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                            rels.append([index_r[0],j, index_r[1], pred_dic[i][1][j]]) # 头 尾 标签 头:标签;
                    for r in rels:
                        # gold里面需要加2，因为从1开始，j是从0开始，需要加3
                        # if r[3] in extra_not_pred_rel:
                        #     f1.write("\\depedge[edge style={red!40,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}"+"\n")
                        #     print("\\depedge[edge style={red!40,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}")
                        if r[3] in extra_not_gold_rel:
                            f1.write("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}")   
                        elif r[3] in extra_diff_pred:
                            f1.write("\\depedge[edge style={red,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={red,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}")   
                        else:
                            f1.write("\\depedge[edge style={black,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={black,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}")
                num+=1
                f1.write("\\end{dependency}\n\\label{fig:dang-zuo-fenci}\n\\end{center}\n\\end{figure}\n")
                f1.write("\n")
                print("\\end{dependency}\n\\label{fig:dang-zuo-fenci}\n\\end{center}\n\\end{figure}\n")
                print("\n")
    
    f1.write("--------------------分割线2------------------------\n\n")    
    for i in diff_dic.keys():
        if i not in extra_s_dic.keys(): # 如果没有预测到论元的句子做过了，预测多论元的句子就不再做了
            extra_s_dic[i] = 0 # 加进去，最后extra_s_dic应该是句子的总个数
            extra_not_pred_rel, extra_not_gold_rel, extra_diff = [], [], [] # 预测没预测到的论元, 预测多的论元, 两者标注不同的论元
            for e in diff_dic[i]:# 如果也是存在预测和gold不同的论元的句子
                extra_diff_gold.append(e[2])
                extra_diff_pred.append(e[3])
            if i in not_pred_dic.keys(): # 如果是没预测到论元的句子
                for e in not_pred_dic[i]:
                    extra_not_pred_rel.append(e[2])
            if i in not_gold_dic.keys():# 如果多预测到论元
                for e in not_gold_dic[i]:
                    extra_not_gold_rel.append(e[3])
            if len(i.split()) <= 10:
                # overleaf框架前半部分
                f1.write("\\begin{figure}[htbp]\n\\begin{center}\n\\begin{dependency}[arc edge, arc angle=80, text only label, label style={above}]\n\\begin{deptext} [row sep=0.2cm, column sep=.5cm]\n")
                f1.write("\\&Root\\&"+"\\&".join(i.split())+r'\\'+"\n")
                f1.write("\\end{deptext}\n")

                print("\\begin{figure}[htbp]\n\\begin{center}\n\\begin{dependency}[arc edge, arc angle=80, text only label, label style={above}]\n\\begin{deptext} [row sep=0.2cm, column sep=.5cm]\n")
                # 输出句子
                print("\\&Root\\&"+"\\&".join(i.split())+r'\\'+"\n")
                print("\\end{deptext}\n")
                # note overleaf里面 root的下标从2开始,上面的标注是gold，下面的标注是predict
                if i in gold_dic.keys(): # 输出gold的标注
                    rels = []
                    for j in range(len(gold_dic[i][1])):
                        if gold_dic[i][1][j] != "_":
                            index_r = gold_dic[i][1][j].split(":")
                            # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                            rels.append([index_r[0],j, index_r[1], gold_dic[i][1][j]]) # 头 尾 标签 头:标签;
                    for r in rels:
                        # gold里面需要加2，因为从1开始，j是从0开始，需要加3
                        if r[3] in extra_not_pred_rel:
                            f1.write("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}")
                        # elif r[3] in extra_not_gold_rel:
                        #     f1.write("\\depedge[edge style={blue,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}"+"\n")
                        #     print("\\depedge[edge style={blue,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}")   
                        elif r[3] in extra_diff_gold:
                            f1.write("\\depedge[edge style={red,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={red,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}")   
                        else:
                            f1.write("\\depedge[edge style={black,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={black,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}")
                if i in pred_dic.keys(): # 输出预测的标注
                    rels = []
                    for j in range(len(pred_dic[i][1])):
                        if pred_dic[i][1][j] != "_":
                            index_r = pred_dic[i][1][j].split(":")
                            # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                            rels.append([index_r[0],j, index_r[1], pred_dic[i][1][j]]) # 头 尾 标签 头:标签;
                    for r in rels:
                        # gold里面需要加2，因为从1开始，j是从0开始，需要加3
                        # if r[3] in extra_not_pred_rel:
                        #     f1.write("\\depedge[edge style={red!40,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}"+"\n")
                        #     print("\\depedge[edge style={red!40,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}")
                        if r[3] in extra_not_gold_rel:
                            f1.write("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}")   
                        elif r[3] in extra_diff_pred:
                            f1.write("\\depedge[edge style={red,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={red,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}")   
                        else:
                            f1.write("\\depedge[edge style={black,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={black,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}")
                num+=1
                f1.write("\\end{dependency}\n\\label{fig:dang-zuo-fenci}\n\\end{center}\n\\end{figure}\n")
                f1.write("\n")
                print("\\end{dependency}\n\\label{fig:dang-zuo-fenci}\n\\end{center}\n\\end{figure}\n")
                print("\n")
    
    print(num)
    
    f1.close()

def get_orig_sen_singleP(file):
    # 获得单个谓词的数据，统计词数和句子数
    with open(file, encoding="UTF-8") as f:
        # 第二行是lemma 原型
        word_num, rel_num, repeat, num_no_p = 0, 0, 0, 0
        sentences, words, relations, dic = [], [], [], {}
        # 先找谓词
        for line in f:
            temp = line.strip().split("\t")
            if len(temp) == 1:
                sentences.append([words, relations])
                word_num += len(words)
                rel_num += len(relations)
                words, relations = [], []
            else:
                words.append(temp[1])
                relations.append(temp[8])
        for s in sentences:
            # print(s)
            temp_s = " ".join(s[0])
            temp_labels = s[1]
            flag = 0
            for idx in range(len(temp_labels)):
                if temp_labels[idx] == "0:[prd]":
                    temp_p = idx+1 # 谓词从1开始计算
                    flag = 1
                    break
            if flag == 0: # 无谓词的情况
                temp_p = 0
                num_no_p += 1
                # print(s)
            if "\t".join([temp_s, str(temp_p)]) not in dic.keys():
                dic["\t".join([temp_s, str(temp_p)])] = s
            else:
                repeat += 1

        print(f"谓词数：{len(dic)}")
        print(f"没有谓词的句子数：{num_no_p}")
        print(f"重复的谓词数：{repeat}")

    return sentences, dic

def compare_right_rel_singleP(s_gold, s_pred):
    # 获得预测和gold不同的标注,每个key是句子
    all_, same, no_pre, not_gold, diff, all_diff = 0, 0, 0, 0, 0, 0
    dic_not_pred, dic_not_gold, dic_diff, = {}, {}, {}
    for i in s_gold.keys():
        if i in s_pred.keys():
            for j in range(len(s_pred[i][1])):
                all_ += 1
                if s_pred[i][1][j] == s_gold[i][1][j]:# 包含-和标注的情况,相同情况
                    same += 1                   
                else:
                    # 预测没有情况
                    all_diff += 1
                    if s_pred[i][1][j] == "_" and s_gold[i][1][j] != "_": # 需要预测但没有预测到的论元
                        no_pre += 1
                        # 存在词典里[下标，词，gold标签，pred标签]。下标是从0开始
                        if i not in dic_not_pred.keys():
                            dic_not_pred[i]=[]
                            dic_not_pred[i].append([j, s_gold[i][0][j], s_gold[i][1][j], "_"])
                        else:
                            dic_not_pred[i].append([j, s_gold[i][0][j], s_gold[i][1][j], "_"])
                    elif s_pred[i][1][j] != "_" and s_gold[i][1][j] == "_": # 不需要预测的论元（多预测的论元）
                        not_gold += 1
                        # 存在词典里
                        if i not in dic_not_gold.keys():
                            dic_not_gold[i]=[]
                            dic_not_gold[i].append([j, s_gold[i][0][j], "_", s_pred[i][1][j]])
                        else:
                            dic_not_gold[i].append([j, s_gold[i][0][j], "_", s_pred[i][1][j]])
                    elif s_pred[i][1][j] != "_" and s_gold[i][1][j] != "_": # 需要预测，但预测错误的论元
                        diff += 1
                        # 存在词典里
                        if i not in dic_diff.keys():
                            dic_diff[i]=[]
                            dic_diff[i].append([j, s_gold[i][0][j], s_gold[i][1][j], s_pred[i][1][j]])
                        else:
                            dic_diff[i].append([j, s_gold[i][0][j], s_gold[i][1][j], s_pred[i][1][j]])
        else:
            print("error! dismatch between training and predict!")
    print(f"标注的词的个数有：{all_}")
    print(f"标签不相同的词的个数：{all_diff}")
    print(f"需要预测但没有预测到的结果个数：{not_gold}个, {len(dic_not_gold)}句；")
    print(f"不需要预测但多预测的结果个数：{no_pre}个,{len(dic_not_pred)}句；")
    print(f"在需要预测的结果中，预测错误的结果个数：{diff}个, {len(dic_diff)}句；")
    return dic_not_gold, dic_not_pred, dic_diff

def get_dic_gold_singleP(not_pred_dic, not_gold_dic, diff_dic, gold_dic, pred_dic, file, num_words=10):
    f1 = open(file, "w", encoding="utf-8")
    num = 0
    extra_s_dic = {}
    for i in not_pred_dic.keys():
        if i not in extra_s_dic.keys(): # 如果没有预测到论元的句子做过了，预测多论元中重复的句子就不再做了
            extra_s_dic[i] = 0
        # extra_not_pred_rel, extra_not_gold_rel, extra_diff= [], [], []# 预测没预测到的论元, 预测多的论元, 两者标注不同的论元
        extra_not_pred_rel, extra_not_gold_rel, extra_diff_gold, extra_diff_pred = {}, {}, {}, {} # 可以根据下标和头来判断是否多标注或少标注
        # note:每个词典里的value元素都是[index，词, gold_label, predict_label]
        for e in not_pred_dic[i]:
            extra_not_pred_rel["\t".join([str(e[0]),e[2]])] = 0 #key 由下标和gold标签组成
            # extra_not_pred_rel.append([e[0],e[2]]) # 
        if i in not_gold_dic.keys(): # 如果是多预测论元的句子
            for e in not_gold_dic[i]:
                extra_not_gold_rel["\t".join([str(e[0]),e[3]])] = 0#key 由下标和pred标签组成
                # extra_not_gold_rel.append([e[0], e[3]]) 
        if i in diff_dic.keys():# 如果也是存在预测和gold不同的论元的句子
            for e in diff_dic[i]:
                extra_diff_gold["\t".join([str(e[0]),e[2]])] = 0
                extra_diff_pred["\t".join([str(e[0]),e[3]])] = 0
                # extra_diff.append([e[0],e[2], e[3]])
        if len(i.split()) <= num_words:
            # overleaf框架前半部分
            f1.write("\\begin{figure}[htbp]\n\\begin{center}\n\\begin{dependency}[arc edge, arc angle=80, text only label, label style={above}]\n\\begin{deptext} [row sep=0.2cm, column sep=.5cm]\n")
            f1.write("\\&Root\\&"+"\\&".join(i.split())+r'\\'+"\n")
            f1.write("\\end{deptext}\n")
            print("\\begin{figure}[htbp]\n\\begin{center}\n\\begin{dependency}[arc edge, arc angle=80, text only label, label style={above}]\n\\begin{deptext} [row sep=0.2cm, column sep=.5cm]\n")
            # 输出句子
            print("\\&Root\\&"+"\\&".join(i.split())+r'\\'+"\n")
            print("\\end{deptext}\n")
            # note overleaf里面 root的下标从2开始,上面的标注是gold，下面的标注是predict
            if i in gold_dic.keys(): # 输出gold的标注
                rels = []
                for j in range(len(gold_dic[i][1])): # 将该句子中gold的标签都获得
                    if gold_dic[i][1][j] != "_":
                        index_r = gold_dic[i][1][j].split(":")
                        # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                        rels.append([index_r[0], j, index_r[1], gold_dic[i][1][j]]) # 头 ，尾 ，标签， 头:标签;
                for r in rels:
                    # gold里面需要加2，因为从1开始，j是从0开始，需要加3
                    # if r[3] in extra_not_pred_rel:
                    if "\t".join([str(r[1]),r[3]]) in extra_not_pred_rel.keys(): # pred没有预测到的gold中的标签
                        f1.write("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}"+"\n")
                        print("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}")
                    elif "\t".join([str(r[1]),r[3]]) in extra_not_pred_rel.keys():
                        print("error1!")
                        exit()
                    # elif r[3] in extra_not_gold_rel:
                    #     f1.write("\\depedge[edge style={blue,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}"+"\n")
                    #     print("\\depedge[edge style={blue,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}")   
                    # elif r[3] in extra_diff_gold:
                    elif "\t".join([str(r[1]),r[3]]) in extra_diff_gold.keys():
                        f1.write("\\depedge[edge style={red,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}"+"\n")
                        print("\\depedge[edge style={red,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}")   
                    else:
                        f1.write("\\depedge[edge style={black,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}"+"\n")
                        print("\\depedge[edge style={black,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}")
            else:
                print("error!")
            if i in pred_dic.keys(): # 输出预测的标注
                rels = []
                for j in range(len(pred_dic[i][1])):
                    if pred_dic[i][1][j] != "_":
                        index_r = pred_dic[i][1][j].split(":")
                        # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                        rels.append([index_r[0], j, index_r[1], pred_dic[i][1][j]]) # 头 尾 标签 头:标签;
                for r in rels:
                    # gold里面需要加2，因为从1开始，j是从0开始，需要加3
                    # if r[3] in extra_not_pred_rel:
                    #     f1.write("\\depedge[edge style={red!40,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}"+"\n")
                    #     print("\\depedge[edge style={red!40,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}")
                    # if r[3] in extra_not_gold_rel:
                    if "\t".join([str(r[1]),r[3]]) in extra_not_gold_rel.keys():
                        f1.write("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}"+"\n")
                        print("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}")   
                    elif "\t".join([str(r[1]),r[3]]) in extra_diff_pred.keys():
                        f1.write("\\depedge[edge style={red,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}"+"\n")
                        print("\\depedge[edge style={red,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}")   
                    elif "\t".join([str(r[1]),r[3]]) in extra_not_pred_rel.keys():
                        print(j)
                        print(gold_dic[i])
                        print(pred_dic[i])
                        print(extra_not_pred_rel)
                        print("error2!")
                        exit()
                    else:
                        f1.write("\\depedge[edge style={black,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}"+"\n")
                        print("\\depedge[edge style={black,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}")
            num+=1
            f1.write("\\end{dependency}\n\\label{fig:dang-zuo-fenci}\n\\end{center}\n\\end{figure}\n")
            f1.write("\n")
            print("\\end{dependency}\n\\label{fig:dang-zuo-fenci}\n\\end{center}\n\\end{figure}\n")
            print("\n")
    
    f1.write("--------------------分割线1------------------------\n\n")
    for i in not_gold_dic.keys():
        if i not in extra_s_dic.keys(): # 如果没有预测到论元的句子做过了，预测多论元的句子就不再做了
            extra_s_dic[i] = 0 # 加进去，看只有论元不同的句子去做
            extra_not_pred_rel, extra_not_gold_rel, extra_diff_gold, extra_diff_pred = {}, {}, {}, {} # 预测没预测到的论元, 预测多的论元, 两者标注不同的论元
            for e in not_gold_dic[i]:
                extra_not_gold_rel["\t".join([str(e[0]),e[2]])] = 0 #key 由下标和gold标签组成
                # extra_not_pred_rel.append([e[0],e[2]]) # 
            if i in not_pred_dic.keys(): # 如果是多预测论元的句子
                for e in not_pred_dic[i]:
                    extra_not_pred_rel["\t".join([str(e[0]),e[3]])] = 0#key 由下标和pred标签组成
                    # extra_not_gold_rel.append([e[0], e[3]]) 
            if i in diff_dic.keys():# 如果也是存在预测和gold不同的论元的句子
                for e in diff_dic[i]:
                    extra_diff_gold["\t".join([str(e[0]),e[2]])] = 0
                    extra_diff_pred["\t".join([str(e[0]),e[3]])] = 0
            # for e in not_gold_dic[i]:
            #     extra_not_gold_rel.append(e[3])
            # if i in not_pred_dic.keys(): # 如果是多预测论元的句子
            #     for e in not_pred_dic[i]:
            #         extra_not_pred_rel.append(e[2])
            # if i in diff_dic.keys():# 如果也是存在预测和gold不同的论元的句子
            #     for e in dic_diff[i]:
            #         extra_diff_gold.append(e[2])
            #         extra_diff_pred.append(e[3])
            if len(i.split()) <= num_words:
                # overleaf框架前半部分
                f1.write("\\begin{figure}[htbp]\n\\begin{center}\n\\begin{dependency}[arc edge, arc angle=80, text only label, label style={above}]\n\\begin{deptext} [row sep=0.2cm, column sep=.5cm]\n")
                f1.write("\\&Root\\&"+"\\&".join(i.split())+r'\\'+"\n")
                f1.write("\\end{deptext}\n")

                print("\\begin{figure}[htbp]\n\\begin{center}\n\\begin{dependency}[arc edge, arc angle=80, text only label, label style={above}]\n\\begin{deptext} [row sep=0.2cm, column sep=.5cm]\n")
                # 输出句子
                print("\\&Root\\&"+"\\&".join(i.split())+r'\\'+"\n")
                print("\\end{deptext}\n")
                # note overleaf里面 root的下标从2开始,上面的标注是gold，下面的标注是predict
                if i in gold_dic.keys(): # 输出gold的标注
                    rels = []
                    for j in range(len(gold_dic[i][1])):
                        if gold_dic[i][1][j] != "_":
                            index_r = gold_dic[i][1][j].split(":")
                            # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                            rels.append([index_r[0],j, index_r[1], gold_dic[i][1][j]]) # 头 尾 标签 头:标签;
                    for r in rels:
                        # gold里面需要加2，因为从1开始，j是从0开始，需要加3
                        # if r[3] in extra_not_pred_rel:
                        if "\t".join([str(r[1]),r[3]]) in extra_not_pred_rel.keys():
                            f1.write("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}")
                        # elif r[3] in extra_diff_gold:
                        elif "\t".join([str(r[1]),r[3]]) in extra_diff_gold.keys():
                            f1.write("\\depedge[edge style={red,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={red,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}")   
                        else:
                            f1.write("\\depedge[edge style={black,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={black,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}")
                        # else:
                        #     f1.write("\\depedge[edge style={black,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}"+"\n")
                        #     print("\\depedge[edge style={black,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}")
                if i in pred_dic.keys(): # 输出预测的标注
                    rels = []
                    for j in range(len(pred_dic[i][1])):
                        if pred_dic[i][1][j] != "_":
                            index_r = pred_dic[i][1][j].split(":")
                            # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                            rels.append([index_r[0],j, index_r[1], pred_dic[i][1][j]]) # 头 尾 标签 头:标签;
                    for r in rels:
                        # gold里面需要加2，因为从1开始，j是从0开始，需要加3
                        if "\t".join([str(r[1]),r[3]]) in extra_not_gold_rel.keys():
                            f1.write("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}")   
                        elif "\t".join([str(r[1]),r[3]]) in extra_diff_pred.keys():
                            f1.write("\\depedge[edge style={red,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={red,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}")   
                        else:
                            f1.write("\\depedge[edge style={black,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={black,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}")
                num+=1
                f1.write("\\end{dependency}\n\\label{fig:dang-zuo-fenci}\n\\end{center}\n\\end{figure}\n")
                f1.write("\n")
                print("\\end{dependency}\n\\label{fig:dang-zuo-fenci}\n\\end{center}\n\\end{figure}\n")
                print("\n")
    
    f1.write("--------------------分割线2------------------------\n\n")    
    for i in diff_dic.keys():
        if i not in extra_s_dic.keys(): # 如果没有预测到论元的句子做过了，预测多论元的句子就不再做了
            extra_s_dic[i] = 0 # 加进去，最后extra_s_dic应该是句子的总个数
            extra_not_pred_rel, extra_not_gold_rel, extra_diff_gold, extra_diff_pred = {},{},{},{} # 预测没预测到的论元, 预测多的论元, 两者标注不同的论元
            for e in diff_dic[i]:# 如果也是存在预测和gold不同的论元的句子
                extra_diff_gold["\t".join([str(e[0]),e[2]])] = 0
                extra_diff_pred["\t".join([str(e[0]),e[3]])] = 0
            if i in not_pred_dic.keys(): # 如果是多预测论元的句子
                for e in not_pred_dic[i]:
                    extra_not_pred_rel["\t".join([str(e[0]),e[3]])] = 0#key 由下标和pred标签组成
                    # extra_not_gold_rel.append([e[0], e[3]]) 
            if i in dic_not_gold.keys():# 如果也是存在预测和gold不同的论元的句子
                for e in dic_not_gold[i]:
                    extra_not_gold_rel["\t".join([str(e[0]),e[2]])] = 0#key 由下标和pred标签组成        
            if len(i.split()) <= num_words:
                # overleaf框架前半部分
                f1.write("\\begin{figure}[htbp]\n\\begin{center}\n\\begin{dependency}[arc edge, arc angle=80, text only label, label style={above}]\n\\begin{deptext} [row sep=0.2cm, column sep=.5cm]\n")
                f1.write("\\&Root\\&"+"\\&".join(i.split())+r'\\'+"\n")
                f1.write("\\end{deptext}\n")

                print("\\begin{figure}[htbp]\n\\begin{center}\n\\begin{dependency}[arc edge, arc angle=80, text only label, label style={above}]\n\\begin{deptext} [row sep=0.2cm, column sep=.5cm]\n")
                # 输出句子
                print("\\&Root\\&"+"\\&".join(i.split())+r'\\'+"\n")
                print("\\end{deptext}\n")
                # note overleaf里面 root的下标从2开始,上面的标注是gold，下面的标注是predict
                if i in gold_dic.keys(): # 输出gold的标注
                    rels = []
                    for j in range(len(gold_dic[i][1])):
                        if gold_dic[i][1][j] != "_":
                            index_r = gold_dic[i][1][j].split(":")
                            # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                            rels.append([index_r[0],j, index_r[1], gold_dic[i][1][j]]) # 头 尾 标签 头:标签;
                    for r in rels:
                        # gold里面需要加2，因为从1开始，j是从0开始，需要加3
                        if "\t".join([str(r[1]),r[3]]) in extra_not_pred_rel.keys():
                        # if r[3] in extra_not_pred_rel:
                            f1.write("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}")
                        # elif r[3] in extra_not_gold_rel:
                        #     f1.write("\\depedge[edge style={blue,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}"+"\n")
                        #     print("\\depedge[edge style={blue,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}")   
                        elif "\t".join([str(r[1]),r[3]]) in extra_diff_gold.keys():
                            f1.write("\\depedge[edge style={red,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={red,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}")   
                        else:
                            f1.write("\\depedge[edge style={black,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={black,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}")
                if i in pred_dic.keys(): # 输出预测的标注
                    rels = []
                    for j in range(len(pred_dic[i][1])):
                        if pred_dic[i][1][j] != "_":
                            index_r = pred_dic[i][1][j].split(":")
                            # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                            rels.append([index_r[0],j, index_r[1], pred_dic[i][1][j]]) # 头 尾 标签 头:标签;
                    for r in rels:
                        # gold里面需要加2，因为从1开始，j是从0开始，需要加3
                        # if r[3] in extra_not_pred_rel:
                        #     f1.write("\\depedge[edge style={red!40,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}"+"\n")
                        #     print("\\depedge[edge style={red!40,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}")
                        if "\t".join([str(r[1]),r[3]]) in extra_not_gold_rel.keys():
                            f1.write("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}")   
                        elif "\t".join([str(r[1]),r[3]]) in extra_diff_pred.keys():
                            f1.write("\\depedge[edge style={red,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={red,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red}"+r[2]+"}")   
                        else:
                            f1.write("\\depedge[edge style={black,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={black,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{black}"+r[2]+"}")
                num+=1
                f1.write("\\end{dependency}\n\\label{fig:dang-zuo-fenci}\n\\end{center}\n\\end{figure}\n")
                f1.write("\n")
                print("\\end{dependency}\n\\label{fig:dang-zuo-fenci}\n\\end{center}\n\\end{figure}\n")
                print("\n")
    
    right_num = 0
    for i in gold_dic.keys(): # 其他全部正确的数据
        if i not in extra_s_dic.keys(): # 如果没有预测到论元的句子做过了，预测多论元中重复的句子就不再做了
            right_num += 1
            extra_s_dic[i] = 0
            # extra_not_pred_rel, extra_not_gold_rel, extra_diff= [], [], []# 预测没预测到的论元, 预测多的论元, 两者标注不同的论元
            extra_not_pred_rel, extra_not_gold_rel, extra_diff_gold, extra_diff_pred = {}, {}, {}, {} # 可以根据下标和头来判断是否多标注或少标注
            # note:每个词典里的value元素都是[index，词, gold_label, predict_label]
            if i in not_pred_dic.keys():
                for e in not_pred_dic[i]:
                    extra_not_pred_rel["\t".join([str(e[0]),e[2]])] = 0 #key 由下标和gold标签组成
                # extra_not_pred_rel.append([e[0],e[2]]) # 
            if i in not_gold_dic.keys(): # 如果是多预测论元的句子
                for e in not_gold_dic[i]:
                    extra_not_gold_rel["\t".join([str(e[0]),e[3]])] = 0#key 由下标和pred标签组成
                    # extra_not_gold_rel.append([e[0], e[3]]) 
            if i in diff_dic.keys():# 如果也是存在预测和gold不同的论元的句子
                for e in diff_dic[i]:
                    extra_diff_gold["\t".join([str(e[0]),e[2]])] = 0
                    extra_diff_pred["\t".join([str(e[0]),e[3]])] = 0  
        # print(len(extra_not_pred_rel), len(extra_not_gold_rel), len(extra_diff_gold), len(extra_diff_pred))      
    print(num)
    print(right_num, right_num+num)
    print(len(gold_dic))
    print(len(extra_s_dic))
    f1.close()

if __name__=="__main__":
    pred_conll05_wjs = "/data/yhliu/SRL-as-GP/predict/BES-wsj-conll05.pred"
    gold_conll05_wjs = "/data/yhliu/SRL-as-GP/data/BES/conll05/BES-wsj.conllu"
    # 原始句子中的统计
    # predictions,pred_dic = get_orig_sen(pred_conll05_wjs) 
    # golds,gold_dic = get_orig_sen(gold_conll05_wjs)

    # 句子转成单个谓词后进行的统计
    conll05wjs_single = config["conll05wjs_single"]
    conll05wjs_pre_single = config["conll05wjs_pred_single"]
    predictions,pred_dic = get_orig_sen_singleP(conll05wjs_pre_single)
    golds,gold_dic = get_orig_sen_singleP(conll05wjs_single)
    dic_not_gold, dic_not_pred, dic_diff = compare_right_rel_singleP(gold_dic, pred_dic)
    file_1 = "/data/yhliu/SRL-as-GP/analysis/not_pred.conll"
    get_dic_gold_singleP(dic_not_pred, dic_not_gold, dic_diff, gold_dic, pred_dic, file_1, 1000)

