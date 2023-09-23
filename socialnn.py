import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping

# Load your data from the Excel file
df = pd.read_excel('socialnndataset.xlsx')

# Handle missing values by filling them with an empty string
df['Tweets'].fillna('', inplace=True)

# Split the data into 90% training and 10% testing samples
train_data, test_data, train_labels, test_labels = train_test_split(
    df['Tweets'], df['Type'], test_size=0.1, random_state=42
)

# Initialize and fit a tokenizer on the training data
tokenizer = Tokenizer(num_words=5000)  # You can adjust the 'num_words' based on your dataset size
tokenizer.fit_on_texts(train_data)

# Convert text data to sequences and pad them to have a fixed length
train_sequences = tokenizer.texts_to_sequences(train_data)
test_sequences = tokenizer.texts_to_sequences(test_data)

max_sequence_length = 100  # You can adjust this based on your data
train_sequences = pad_sequences(train_sequences, maxlen=max_sequence_length)
test_sequences = pad_sequences(test_sequences, maxlen=max_sequence_length)

model = Sequential()

# Add an Embedding layer for word embeddings
model.add(Embedding(input_dim=5000, output_dim=100, input_length=max_sequence_length))

# Add LSTM layers for sequence processing
model.add(LSTM(units=100))

# Add a Dense layer for binary classification
model.add(Dense(units=1, activation='sigmoid'))

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Print the model summary
model.summary()

# Convert string labels to binary labels
train_labels = np.array([1 if label == 'Random' else 0 for label in train_labels])
test_labels = np.array([1 if label == 'Random' else 0 for label in test_labels])

# Early Stopping
early_stopping = EarlyStopping(monitor='val_loss', patience=3)

# Train the model on the training data
history = model.fit(train_sequences, train_labels, epochs=50, batch_size=64, validation_split=0.2, callbacks=[early_stopping])

# Evaluate the model on the testing data
test_loss, test_accuracy = model.evaluate(test_sequences, test_labels)
print(f"Test accuracy: {test_accuracy * 100:.2f}%")

# Make predictions on the test data
predictions = model.predict(test_sequences)

# Convert predictions to class labels ('Random' or 'Disaster')
predicted_labels = ['Random' if pred >= 0.5 else 'Disaster' for pred in predictions]

import tweepy

# credentials
consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'
access_token = 'access_token'
access_token_secret = 'access_token_secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

keyword = 'disaster'  # add a keyword list here
tweets = api.search(q=keyword, count=10)

for tweet in tweets:
    tweetList.append(tweet.text)

input_data = np.array(tweetList)
predictions = model.predict(input_data)
for i, prediction in enumerate(predictions):
    print(f"Prediction {i + 1}: {prediction}")







