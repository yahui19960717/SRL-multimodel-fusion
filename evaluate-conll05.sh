
CUDA_VISIBLE_DEVICES=3 python -m supar.cmds.vi_SRL evaluate\
        -p exp/BES-base-model-givenpred/model \
        --data predict/BES-wsj.pred \
        --schema BES \
        -d 3



#  /data/yhliu/SRL-MultiModelFusion/model_ensemble/voting_result/voting_bes_be_latent.conllu \