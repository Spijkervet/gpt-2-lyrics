TRAIN_FILE=lyrics.txt
echo $TRAIN_FILE

python run_language_modeling.py \
    --output_dir=lyrics \
    --model_type=gpt2 \
    --model_name_or_path=gpt2-medium \
    --do_train \
    --train_data_file=$TRAIN_FILE \
    --num_train_epochs=10 \
    --per_gpu_train_batch_size=1 \
    --block_size=512 \
    --logging_steps=1 \
    --learning_rate=0.0001 \
    # --fp16
    # --gradient_accumulation_steps=5 \
