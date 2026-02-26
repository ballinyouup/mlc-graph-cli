#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

mkdir -p "$PROJECT_ROOT/PGraphRAG"
cd "$PROJECT_ROOT/PGraphRAG"

# Amazon Reviews dataset for All Beauty Category.
wget https://raw.githubusercontent.com/PGraphRAG-benchmark/PGraphRAG/refs/heads/main/data_splits/amazon_train.json
wget https://raw.githubusercontent.com/PGraphRAG-benchmark/PGraphRAG/refs/heads/main/data_splits/amazon_dev.json
wget https://raw.githubusercontent.com/PGraphRAG-benchmark/PGR-LLM/refs/heads/main/data_splits/amazon_test.json

# Hotel Reviews dataset from Kaggle.
wget https://raw.githubusercontent.com/PGraphRAG-benchmark/PGraphRAG/refs/heads/main/data_splits/hotel_train.json
wget https://raw.githubusercontent.com/PGraphRAG-benchmark/PGraphRAG/refs/heads/main/data_splits/hotel_dev.json
wget https://raw.githubusercontent.com/PGraphRAG-benchmark/PGraphRAG/refs/heads/main/data_splits/hotel_test.json

# Grammar and Online Product Reviews dataset from Kaggle.
wget https://raw.githubusercontent.com/PGraphRAG-benchmark/PGraphRAG/refs/heads/main/data_splits/gap_train.json
wget https://raw.githubusercontent.com/PGraphRAG-benchmark/PGraphRAG/refs/heads/main/data_splits/gap_dev.json
wget https://raw.githubusercontent.com/PGraphRAG-benchmark/PGraphRAG/refs/heads/main/data_splits/gap_test.json

# B2W-Reviews dataset from github.
wget https://raw.githubusercontent.com/PGraphRAG-benchmark/PGraphRAG/refs/heads/main/data_splits/b2w_train.json
wget https://raw.githubusercontent.com/PGraphRAG-benchmark/PGraphRAG/refs/heads/main/data_splits/b2w_dev.json
wget https://raw.githubusercontent.com/PGraphRAG-benchmark/PGraphRAG/refs/heads/main/data_splits/b2w_test.json

# Finetune: Download Ministral-3-3B-Instruct-2512 model from Huggingface.
mkdir -p "$PROJECT_ROOT/models"
cd "$PROJECT_ROOT/models"
git clone https://huggingface.co/MistralAI/Ministral-3-3B-Instruct-2512

# Extract: Download Ministral-3-3B-Instruct-2512 model from Huggingface.
mkdir -p "$PROJECT_ROOT/models"
cd "$PROJECT_ROOT/models"
git clone https://huggingface.co/mlc-ai/Ministral-3-3B-Instruct-2512-BF16-q4f16_1-MLC

