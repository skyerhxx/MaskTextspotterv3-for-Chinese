#调整GPU数: 修改--nproc_per_node
python -m torch.distributed.launch --nproc_per_node=4 tools/train_net.py \
        --config-file configs/mixtrain/seg_rec_poly_fuse_feature_chinese_train.yaml