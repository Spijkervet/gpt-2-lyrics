
export TRAIN_FILE=lyrics.txt

python run_language_modeling.py \
    --output_dir=lyrics_e2 \
    --model_type=gpt2 \
    --model_name_or_path=gpt2-medium \
    --do_train \
    --train_data_file=$TRAIN_FILE \
    --num_train_epochs=2 \
    --per_gpu_train_batch_size=1 \
    --block_size=256
