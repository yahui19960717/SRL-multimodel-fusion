
CUDA_VISIBLE_DEVICES=3 python -m supar.cmds.vi_SRL train -b \
        --train data/BIES-conll05/BIES-train.conllu\
        --dev   data/BIES-conll05/BIES-dev.conllu  \
        --test  data/BIES-conll05/BIES-wsj.conllu \
        --batch-size 2000 \
        --n-embed 100 \
        --feat lemma,char \
        --itp 0.06 \
        --embed data/glove.6B.300d.txt \
        --n_pretrained_embed 300\
        --min_freq 7 \
        --seed 1 \
        --schema BIES \
        --unk "" \
        --train_given_prd \
        -p exp/BIES-base-model-givenpred/model \
        -d 3