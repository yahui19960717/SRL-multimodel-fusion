# 统计误标注核心论元的占比：错误论元占全部论元的个数；论元多标注；论元没标注；论元错标注的情况
# 什么情况下是核心论元？看下规范
# frame是根据sense去找的，但是我目前不知道如何测试出该谓词的sense哇
# 评价什么呢？错误论元占全部论元的个数，全部的论元个数；
from analysis_performance import get_orig_sen_singleP, compare_right_rel_singleP
from config import config

def labels_count(dic):
    labels_dic = {}
    i = 0
    for key in dic.keys():
        i += 1
        for l in dic[key][1]:
            if l != "_" and l != "0:[prd]":
                idx_label = l.split(":")
                c_label = idx_label[1]
                if c_label[0] == "E" or c_label[0] == "S":
                    if len(c_label.split("-")[1:]) == 1:
                        if c_label.split("-")[1:][0] not in labels_dic.keys():
                            labels_dic[c_label.split("-")[1:][0]]=0
                    else:
                        temp = "-".join(c_label.split("-")[1:])
                        if temp not in labels_dic.keys():
                            labels_dic[temp] = 0

    print(labels_dic)
    print(len(labels_dic))

def evaluate_scrips(not_pred_dic, not_gold_dic, diff_dic, gold_dic, pred_dic, file, num_words):
    f1 = open(file, "w", encoding="utf-8")
    num = 0
    extra_s_dic = {}
    core_labels = {'A0': 0, 'A1': 0,'A2': 0,'A3': 0,'A4': 0,'A5': 0,'AA': 0,'R-A0': 0, 'R-A1': 0,'R-A2': 0,'R-A3': 0,'R-A4': 0,'R-A5': 0,'R-AA': 0,'C-A0': 0, 'C-A1': 0,'C-A2': 0,'C-A3': 0,'C-A4': 0,'C-A5': 0,'C-AA': 0,}
    gold_nums, pred_nums, less_pred_nums, extra_pred_nums, extra_core_nums, less_core_nums,differ_core_nums,diff_nums = 0, 0, 0, 0, 0, 0, 0,0
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
                        gold_nums += 1
                        index_r = gold_dic[i][1][j].split(":")
                        # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                        rels.append([index_r[0], j, index_r[1], gold_dic[i][1][j]]) # 头 ，尾 ，标签， 头:标签;
                for r in rels:
                    # gold里面需要加2，因为从1开始，j是从0开始，需要加3
                    # if r[3] in extra_not_pred_rel:
                    if "\t".join([str(r[1]),r[3]]) in extra_not_pred_rel.keys(): # pred没有预测到的gold中的标签
                        less_pred_nums += 1
                        if "-".join(r[3].split(":")[1].split("-")[1:]) in core_labels.keys():
                            less_core_nums += 1
                        f1.write("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}"+"\n")
                        print("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}")
                    elif "\t".join([str(r[1]),r[3]]) in extra_not_pred_rel.keys():
                        print("error1!")
                        exit()
                    elif "\t".join([str(r[1]),r[3]]) in extra_diff_gold.keys():
                        diff_nums += 1
                        if "-".join(r[3].split(":")[1].split("-")[1:]) in core_labels.keys():
                            differ_core_nums += 1
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
                        pred_nums += 1
                        # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                        rels.append([index_r[0], j, index_r[1], pred_dic[i][1][j]]) # 头 尾 标签 头:标签;
                for r in rels:
                    if "\t".join([str(r[1]),r[3]]) in extra_not_gold_rel.keys():
                        extra_pred_nums += 1
                        if "-".join(r[3].split(":")[1].split("-")[1:]) in core_labels.keys():
                            extra_core_nums += 1
                        f1.write("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}"+"\n")
                        print("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}")   
                    elif "\t".join([str(r[1]),r[3]]) in extra_diff_pred.keys():
                        diff_nums+=1
                        if "-".join(r[3].split(":")[1].split("-")[1:]) in core_labels.keys():
                            differ_core_nums += 1
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
                            gold_nums += 1
                            # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                            rels.append([index_r[0],j, index_r[1], gold_dic[i][1][j]]) # 头 尾 标签 头:标签;
                    for r in rels:
                        # gold里面需要加2，因为从1开始，j是从0开始，需要加3
                        # if r[3] in extra_not_pred_rel:
                        if "\t".join([str(r[1]),r[3]]) in extra_not_pred_rel.keys():
                            less_pred_nums += 1
                            if "-".join(r[3].split(":")[1].split("-")[1:]) in core_labels.keys():
                                less_core_nums += 1
                            f1.write("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}")
                        # elif r[3] in extra_diff_gold:
                        elif "\t".join([str(r[1]),r[3]]) in extra_diff_gold.keys():
                            diff_nums+=1
                            if "-".join(r[3].split(":")[1].split("-")[1:]) in core_labels.keys():
                                differ_core_nums += 1
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
                            pred_nums+=1
                            # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                            rels.append([index_r[0],j, index_r[1], pred_dic[i][1][j]]) # 头 尾 标签 头:标签;
                    for r in rels:
                        # gold里面需要加2，因为从1开始，j是从0开始，需要加3
                        if "\t".join([str(r[1]),r[3]]) in extra_not_gold_rel.keys():
                            extra_pred_nums+=1
                            if "-".join(r[3].split(":")[1].split("-")[1:]) in core_labels.keys():
                                extra_core_nums += 1
                            f1.write("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}")   
                        elif "\t".join([str(r[1]),r[3]]) in extra_diff_pred.keys():
                            diff_nums+=1
                            if "-".join(r[3].split(":")[1].split("-")[1:]) in core_labels.keys():
                                differ_core_nums += 1
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
                            gold_nums+=1
                            index_r = gold_dic[i][1][j].split(":")
                            # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                            rels.append([index_r[0],j, index_r[1], gold_dic[i][1][j]]) # 头 尾 标签 头:标签;
                    for r in rels:
                        # gold里面需要加2，因为从1开始，j是从0开始，需要加3
                        if "\t".join([str(r[1]),r[3]]) in extra_not_pred_rel.keys():
                            less_pred_nums+=1
                            if "-".join(r[3].split(":")[1].split("-")[1:]) in core_labels.keys():
                                less_core_nums += 1
                            f1.write("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={red!40,thick}]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{red!40}"+r[2]+"}")
                        elif "\t".join([str(r[1]),r[3]]) in extra_diff_gold.keys():
                            diff_nums+=1
                            if "-".join(r[3].split(":")[1].split("-")[1:]) in core_labels.keys():
                                differ_core_nums += 1
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
                            pred_nums+=1
                            # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                            rels.append([index_r[0],j, index_r[1], pred_dic[i][1][j]]) # 头 尾 标签 头:标签;
                    for r in rels:
                        if "\t".join([str(r[1]),r[3]]) in extra_not_gold_rel.keys():
                            extra_pred_nums += 1
                            if "-".join(r[3].split(":")[1].split("-")[1:]) in core_labels.keys():
                                extra_core_nums += 1
                            f1.write("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}"+"\n")
                            print("\\depedge[edge style={blue,thick},edge below]"+"{"+str(int(r[0])+2)+"}"+"{"+str(int(r[1])+3)+"}"+"{\\color{blue}"+r[2]+"}")   
                        elif "\t".join([str(r[1]),r[3]]) in extra_diff_pred.keys():
                            diff_nums+=1
                            if "-".join(r[3].split(":")[1].split("-")[1:]) in core_labels.keys():
                                differ_core_nums += 1                        
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
            rels = []
            for j in range(len(gold_dic[i][1])):
                if gold_dic[i][1][j] != "_":
                    index_r = gold_dic[i][1][j].split(":")
                    gold_nums += 1
                    # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                    rels.append([index_r[0],j, index_r[1], gold_dic[i][1][j]]) # 头 尾 标签 头:标签;
            # note:每个词典里的value元素都是[index，词, gold_label, predict_label]
            rels = []
            for j in range(len(pred_dic[i][1])):
                if pred_dic[i][1][j] != "_":
                    index_r = pred_dic[i][1][j].split(":")
                    pred_nums+=1
                    # temp = "{"+str(j+2)+"}"+"{"+str(int(index_r[0])+2)+"}"+"{\\color{black}"+index_r[1]
                    rels.append([index_r[0],j, index_r[1], pred_dic[i][1][j]]) # 头 尾 标签 头:标签;
                        
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

    print(f"total gold labels:{gold_nums}")
    print(f"total predict labels:{pred_nums}")
    print(f"少预测的数目:{less_pred_nums, less_pred_nums/pred_nums}， 多预测的数目{extra_pred_nums,extra_pred_nums/pred_nums}")
    print(f'少预测的核心数目:{less_core_nums, less_core_nums/less_pred_nums},  多预测的核心数目{extra_core_nums,extra_core_nums/extra_pred_nums}')
    print(f'不同的数目:{diff_nums},  不同的核心数目{differ_core_nums}')
    print((diff_nums+extra_pred_nums)/pred_nums)

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
    # labels_count(gold_dic)
    dic_not_gold, dic_not_pred, dic_diff = compare_right_rel_singleP(gold_dic, pred_dic)
    file_1 = "/data/yhliu/SRL-as-GP/analysis/debug.conll"
    evaluate_scrips(dic_not_pred, dic_not_gold, dic_diff, gold_dic, pred_dic, file_1, 1000)

    exit()

    # train数据的统计
    single_train = "../data/BES/conll05/BES-train-single.conllu"
    gold_train, train_dic = get_orig_sen_singleP(single_train)
    
    labels_count(train_dic)
    

