

CUDA_VISIBLE_DEVICES=2 python -m supar.cmds.vi_SRL train -b \
        --train data/BES/conll05/BES-train.conllu\
        --dev   data/BES/conll05/BES-dev.conllu  \
        --test  data/BES/conll05/BES-wsj.conllu \
        --batch-size 3000 \
        --n-embed 100 \
        --feat lemma,char \
        --itp 0.06 \
        --embed data/glove.6B.300d.txt \
        --n_pretrained_embed 300\
        --min_freq 7 \
        --seed 33 \
        --schema BES \
        --unk "" \
        --train_given_prd \
        -p exp/BES-base-model-givenpred-33/model \
        -d 2


# CUDA_VISIBLE_DEVICES=2 python -m supar.cmds.vi_SRL train -b \
#         --train data/BES/conll05/BES-train.conllu\
#         --dev   data/BES/conll05/BES-dev.conllu  \
#         --test  data/BES/conll05/BES-wsj.conllu \
#         --batch-size 3000 \
#         --n-embed 100 \
#         --feat lemma,char \
#         --itp 0.06 \
#         --embed data/glove.6B.300d.txt \
#         --n_pretrained_embed 300\
#         --min_freq 7 \
#         --seed 33 \
#         --schema BES \
#         --unk "" \
#         --train_given_prd \
#         -p exp/BES-base-model-givenpred-33/model \
#         -d 2
# CUDA_VISIBLE_DEVICES=1 python -m supar.cmds.vi_SRL train -b \
#         --train data/CoNLL09-Chinese/CoNLL_form/test.conllu\
#         --dev data/CoNLL09-Chinese/CoNLL_form/dev.conllu\
#         --test data/CoNLL09-Chinese/CoNLL_form/test.conllu \
#         --batch-size 2500 \
#         --n-embed 100 \
#         --feat char \
#         --itp 0.06 \
#         --embed data/giga.100.txt \
#         --n_pretrained_embed 100\
#         --min_freq 7 \
#         --seed 1 \
#         --schema BES \
#         --unk "" \
#         --train_given_prd \
#         -p exp/debug/model \
#         -d 1
# data/glove.6B.300d.txt english
# --bert ./bert-base-chinese \
# CUDA_VISIBLE_DEVICES=1 python -m supar.cmds.vi_SRL train -b \
#         --train data/CoNLL09-Chinese/CoNLL_form/train.conllu\
#         --dev data/CoNLL09-Chinese/CoNLL_form/dev.conllu\
#         --test data/CoNLL09-Chinese/CoNLL_form/test.conllu \
#         --batch-size 3000 \
#         --n-embed 100 \
#         --itp 0.06 \
#         --embed data/cc.zh.300.vec \
#         --n_pretrained_embed 300 \
#         --min_freq 7 \
#         --seed 1 \
#         --schema BES \
#         --unk "" \
#         --train_given_prd \
#         -p exp/conll09_chinese-srlnotag/model \
#         -d 1


# CUDA_VISIBLE_DEVICES=0 python -m supar.cmds.vi_SRL train -b \
#         --train data/CoNLL09-Chinese/CoNLL_form/train.conllu\
#         --dev data/CoNLL09-Chinese/CoNLL_form/dev.conllu\
#         --test data/CoNLL09-Chinese/CoNLL_form/test.conllu \
#         --batch-size 3000 \
#         --n-embed 100 \
#         --itp 0.06 \
#         --embed data/cc.zh.300.vec \
#         --n_pretrained_embed 300 \
#         --min_freq 7 \
#         --seed 1 \
#         --schema BES \
#         --unk "" \
#         --train_given_prd \
#         -p exp/conll09_chinese-srl-nonfeat/model \
#         -d 0