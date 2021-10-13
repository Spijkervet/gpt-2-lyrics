SOURCE_DIR=$1
echo SOURCE: $SOURCE_DIR

OUTPUT_DIR="runs/$(basename $SOURCE_DIR)"
echo $OUTPUT_DIR

TRAIN_FILE=$SOURCE_DIR/train.txt
TEST_FILE=$SOURCE_DIR/eval.txt


python3 run_clm.py \
    --model_type=gpt2 \
    --model_name_or_path=GroNLP/gpt2-small-dutch \
    --train_file=$TRAIN_FILE \
    --validation_file=$TEST_FILE \
    --do_train \
    --do_eval \
    --per_device_train_batch_size 16 \
    --per_device_eval_batch_size 16 \
    --num_train_epochs 10 \
    --block_size 512 \
    --output_dir $OUTPUT_DIR

# python3 run_language_modeling.py \
#     --output_dir=lyrics \
#     --model_type=gpt2 \
#     --model_name_or_path=gpt2-medium \
#     --do_train \
#     --train_data_file=$TRAIN_FILE \
#     --num_train_epochs=10 \
#     --per_gpu_train_batch_size=1 \
#     --block_size=512 \
#     --logging_steps=1 \
#     --learning_rate=0.0001 \
#     # --fp16
#     # --gradient_accumulation_steps=5 \
