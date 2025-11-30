from random import sample

import pandas as pd
from src.DL_2 import create_sequences

# 如果是纯文本文件，建议直接读取所有内容
with open(r"../corpus.txt", 'r', encoding='utf-8') as file:
    texts = [file.read()]  # 或者按行分割: file.readlines()
sample_texts = ' '.join(texts)

print(create_sequences(sample_texts))
