CUDA_VISIBLE_DEVICES=3 python -m supar.cmds.vi_SRL predict \
        --data data/BES/conll05/BES-wsj.conllu  \
        -p exp/BES-base-model-givenpred/model \
        --pred predict/voting_bes_bes_bes.conllu \
        --batch-size 2000 \
        --gold data/conll05/conll05.test.props.gold.txt \
        --task 05 \
        --schema BES \
        --vtb \
        --given_prd \
        -d 3

# CUDA_VISIBLE_DEVICES=3 python -m supar.cmds.vi_SRL predict \
#         --data data/BE-conll05/sc-conll5-wsj.conllu\
#         -p exp/BE-base-model-givenpred/model \
#         --pred predict/BE-wsj.pred \
#         --gold data/conll05/conll05.test.props.gold.txt \
#         --task 05 \
#         --schema BE \
#         --vtb \
#         -d 3
# CUDA_VISIBLE_DEVICES=3 python -m supar.cmds.vi_SRL predict --data data/BES/conll05/BES-wsj.conllu  \
#         -p exp/srl_knowledge/model \
#         --pred predict/BES-wsj-conll05.pred \
#         --batch-size 2000 \
#         --gold data/conll05/conll05.test.props.gold.txt \
#         --task 05 \
#         --schema BES \
#         --vtb \
#         --given_prd \
#         -d 3
        # --gold data/conll05/conll05.test.props.gold.txt \