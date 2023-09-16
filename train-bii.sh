
CUDA_VISIBLE_DEVICES=3 python -m supar.cmds.vi_SRL train -b \
        --train data/BII-conll05/BII-train.conllu\
        --dev   data/BII-conll05/BII-dev.conllu  \
        --test  data/BII-conll05/BII-wsj.conllu \
        --batch-size 3000 \
        --n-embed 100 \
        --feat lemma,char \
        --itp 0.06 \
        --embed data/glove.6B.300d.txt \
        --n_pretrained_embed 300\
        --min_freq 7 \
        --seed 1 \
        --schema BII \
        --unk "" \
        --train_given_prd \
        -p exp/BII-base-model-givenpred/model \
        -d 3