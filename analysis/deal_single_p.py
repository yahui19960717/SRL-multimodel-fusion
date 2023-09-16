# 之前写的脚本都是针对单个谓词来说的，需要把多个谓词的句子转换成单个论元句子
'''
先找到句子中的谓词，如果是单个谓词，就直接[下标，语义标签]，如果是多个谓词，先找谓词，然后找谓词对应的论元
Note： 没有考虑谓词不存在的句子
'''
from config import config
from analysis_performance import get_orig_sen

def get_single(dic, out_file):
    with open(out_file, "w", encoding="utf-8") as out:
        sen_dic = {}
        for key in dic.keys(): # 对于一个句子，先找到谓词
            dic_p, list_p = {}, []
            # print(dic[key])
            for i in range(len(dic[key][1])):
                if "|" not in dic[key][1][i]:
                    if dic[key][1][i] == "0:[prd]":
                        p_idx = i+1 # 下标从1开始
                        list_p.append(p_idx)
                else:
                    label_list = dic[key][1][i].split("|")
                    for l in label_list:
                        if l == "0:[prd]":
                            p_idx = i+1 # 下标从1开始
                            list_p.append(p_idx)
                
            if len(list_p) == 1: # 单个谓词
                temp = "\t".join([key, str(p_idx)])
                if  temp not in sen_dic.keys():
                    sen_dic[temp] = []
                    for i in range(len(dic[key][1])):
                        sen_dic[temp].append([i+1, dic[key][1][i]])
            elif len(list_p) == 0: # 谓词不存在的情况
                temp = "\t".join([key, '0'])
                if  temp not in sen_dic.keys():
                    sen_dic[temp] = []
                    for i in range(len(dic[key][1])):
                        sen_dic[temp].append([i+1, "_"])
            else: # 多谓词的情况
                for i in list_p: # 遍历谓词下标，从1开始
                    temp = "\t".join([key, str(i)])
                    if temp not in sen_dic.keys():
                        sen_dic[temp] = [] # 将每个谓词放在里面
                        for j in range(len(dic[key][1])): # 遍历标签，找该谓词对应的标签，注意谓词本身
                                if "|" not in dic[key][1][j]: # 只作一个谓词的论元(包含了谓词本身0:[prd])
                                    p_temp = dic[key][1][j].split(":")[0]
                                    if p_temp != "0" and p_temp == str(i):#谓词i的论元
                                        sen_dic[temp].append([j+1, dic[key][1][j]])
                                    elif p_temp == "0"  and (j+1)==i:
                                        sen_dic[temp].append([j+1, dic[key][1][j]])
                                    else:
                                        sen_dic[temp].append([j+1, "_"])
                                else :
                                    temp_labels = dic[key][1][j].split("|")
                                    flag = 0
                                    for l in temp_labels:
                                        p_temp = l.split(":")[0]
                                        if p_temp != "0" and p_temp == str(i):
                                            sen_dic[temp].append([j+1, l])
                                            flag+=1
                                        elif p_temp == "0"  and (j+1)==i:
                                            sen_dic[temp].append([j+1, l])
                                            flag+=1
                                    if flag==0:
                                        sen_dic[temp].append([j+1, "_"])
                                    if flag==2:
                                        print("error!")
                                        
# 2	while	while	_	IN	_	_	_	33:B-AM-ADV	_
        for key in sen_dic.keys():
            for idx in range(len(sen_dic[key])):
                id = sen_dic[key][idx][0]
                label = sen_dic[key][idx][1]
                words = key.split("\t")[0].split()
                out.write("\t".join([str(id),words[idx],words[idx],"_","_","_","_","_",label,"_","\n"]))
            out.write("\n")
    print(len(sen_dic))

def test_debug(dic):
    sen_dic = {}
    for key in dic.keys(): # 对于一个句子，先找到谓词
        dic_p, list_p = {}, []
        # print(dic[key])
        for i in range(len(dic[key][1])):
            if "|" not in dic[key][1][i]:
                if dic[key][1][i] == "0:[prd]":
                    p_idx = i+1 # 下标从1开始
                    list_p.append(p_idx)
            else:
                label_list = dic[key][1][i].split("|")
                for l in label_list:
                    if l == "0:[prd]":
                        p_idx = i+1 # 下标从1开始
                        list_p.append(p_idx)
            
        if len(list_p) == 1: # 单个谓词
            temp = "\t".join([key, str(p_idx)])
            if  temp not in sen_dic.keys():
                sen_dic[temp] = []
                for i in range(len(dic[key][1])):
                    sen_dic[temp].append([i+1, dic[key][1][i]])
        elif len(list_p) == 0: # 谓词不存在的情况
            temp = "\t".join([key, '0'])
            if  temp not in sen_dic.keys():
                sen_dic[temp] = []
                for i in range(len(dic[key][1])):
                    sen_dic[temp].append([i+1, "_"])
        else: # 多谓词的情况
            for i in list_p: # 遍历谓词下标，从1开始
                temp = "\t".join([key, str(i)])
                if temp not in sen_dic.keys():
                    sen_dic[temp] = [] # 将每个谓词放在里面
                    for j in range(len(dic[key][1])): # 遍历标签，找该谓词对应的标签，注意谓词本身
                            if "|" not in dic[key][1][j]: # 只作一个谓词的论元(包含了谓词本身0:[prd])
                                p_temp = dic[key][1][j].split(":")[0]
                                if p_temp != "0" and p_temp == str(i):#谓词i的论元
                                    sen_dic[temp].append([j+1, dic[key][1][j]])
                                elif p_temp == "0"  and (j+1)==i:
                                    sen_dic[temp].append([j+1, dic[key][1][j]])
                                else:
                                    sen_dic[temp].append([j+1, "_"])
                            else :
                                temp_labels = dic[key][1][j].split("|")
                                flag = 0
                                for l in temp_labels:
                                    p_temp = l.split(":")[0]
                                    if p_temp != "0" and p_temp == str(i):
                                        sen_dic[temp].append([j+1, l])
                                        flag+=1
                                    elif p_temp == "0"  and (j+1)==i:
                                        sen_dic[temp].append([j+1, l])
                                        flag+=1
                                if flag==0:
                                    sen_dic[temp].append([j+1, "_"])
                                if flag==2:
                                    print("error!")
    for key in sen_dic.keys():
        print(key)
    return sen_dic    
if __name__=="__main__":


    debug = "../data/BES/conll05/debug.conllu"
    _, de_dic = get_orig_sen(debug)
    # dic = test_debug(de_dic)
    single_debug = "../data/BES/conll05/BES-debug-single.conllu"
    get_single(de_dic, single_debug) 
    exit()

    conll05wjs_org = config["conll05wjs_org"]
    conll05wjs_single = config["conll05wjs_single"]

    conll05wjs_pre_single = config["conll05wjs_pred_single"]
    conll05wjs_pre = config["conll05wjs_pred"]
    _, org_dic = get_orig_sen(conll05wjs_org)
    _, pre_dic = get_orig_sen(conll05wjs_pre)
    get_single(org_dic, conll05wjs_single)
    # get_single(pre_dic, conll05wjs_pre_single)

    exit()

    # train dataset 获得single谓词
    train = "../data/BES/conll05/BES-train.conllu"
    _, org_train_dic = get_orig_sen(train)
    single_train = "../data/BES/conll05/BES-train-single.conllu"
    get_single(org_train_dic, single_train)



