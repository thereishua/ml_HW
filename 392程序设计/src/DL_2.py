from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import TextVectorization,Embedding, GRU, Dense, Bidirectional,Dropout
from tensorflow.keras.regularizers import l2
import numpy as np


# 1. 构建模型
def build_model(max_tokens=2000, sequence_length=5, embedding_dim=64, gru_units=128):
    """构建包含TextVectorization的端到端模型"""
    vectorizer = TextVectorization(
        max_tokens=max_tokens,
        output_mode='int',
        output_sequence_length=sequence_length
    )

    model = Sequential([
        vectorizer,
        Embedding(
            input_dim=max_tokens,  # 或者 max_tokens + 1
            output_dim=embedding_dim,
            mask_zero=True,
            embeddings_regularizer=l2(1e-5)
        ),
        Bidirectional(GRU(gru_units, return_sequences=True, dropout=0.2)),
        Dropout(0.3),
        Bidirectional(GRU(gru_units // 2, return_sequences=False, dropout=0.2)),
        Dropout(0.3),
        Dense(256, activation='relu', kernel_regularizer=l2(1e-5)),
        Dropout(0.4),
        Dense(128, activation='relu', kernel_regularizer=l2(1e-5)),
        Dropout(0.3),
        Dense(max_tokens, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


# 2. 训练模型
def train_model(model, X, y, epochs=5, batch_size=8):
    """训练模型"""
    history = model.fit(
        X, y,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.2,
        verbose=1)
    return history

# 3创建训练序列(AI)
def create_sequences(tokenized_text, window_size=5):
    tokens = tokenized_text.strip().split()
    X, y = [], []
    for i in range(len(tokens) - window_size):
        X.append(' '.join(tokens[i:i + window_size]))
        y.append(tokens[i + window_size])

    # 创建词汇表映射
    unique_tokens = list(set(tokens))
    token_to_id = {token: idx for idx, token in enumerate(unique_tokens)}

    # 转换y为数字标签
    y_numeric = [token_to_id[token] for token in y]

    return np.array(X, dtype=object), np.array(y_numeric)

# 3. 预测下一个词(AI)
def predict_next_word(model, text_prefix, top_k=3):
    """预测下一个词"""
    # 预处理输入文本
    input_text = np.array([text_prefix],dtype=object)
    predictions = model.predict(input_text, verbose=0)[0]

    # 预测
    top_indices = np.argsort(predictions)[-top_k:][::-1]

    vectorization_layer = model.layers[0]
    vocabulary = vectorization_layer.get_vocabulary()

    results = []
    for idx in top_indices:
        if idx < len(vocabulary) and vocabulary[idx] != '' and vocabulary[idx] is not None:
            word = vocabulary[idx]
            probability = predictions[idx]
            results.append((word, probability))

    return results



# 6. 循环文本生成(AI)
def generate_text(model,seed_text, num_words=10):
    """生成文本"""
    generated_text = seed_text

    for _ in range(num_words):
        # 预测下一个词
        next_words = predict_next_word(model, generated_text, top_k=1)
        if next_words:
            next_word = next_words[0][0]
            generated_text += " " + next_word
        else:
            break

    return generated_text


# 使用示例
if __name__ == "__main__":
    # 示例文本数据
    with open(r"../corpus1.txt", 'r', encoding='utf-8') as file:
        texts = [file.read()]
    sample_texts =' '.join(texts)

    SEQUENCE_LENGTH = 3

    X, y = create_sequences(sample_texts, SEQUENCE_LENGTH)
    model = build_model()
    model.layers[0].adapt(X)  # 适配TextVectorization层

    X = np.array(X, dtype=object)

    history = train_model(model, X, y, epochs=50)

    # 预测下一个词
    next_words = predict_next_word(model, "深度 学习")
    print("Predicted next words:", next_words)

    # 生成一段文本
    generated = generate_text(model, "深度 学习", num_words=20)
    print("Generated text:", generated)