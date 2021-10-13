MODEL_PATH=$1

python3 run_generation.py \
    --model_type=gpt2 \
    --model_name_or_path=$MODEL_PATH \
    --length=256
