1) How to run the program

i) Make sure you have the following files:
train.csv (training data)
test.csv (testing data)
stopwords.txt (list of stopwords)

ii) Install matplotlib if you haven't:
pip install matplotlib

iii) Run the program with:
python nbc_sentiment.py

The program will automatically:
-Execute Task 1 (feature selection)
-Execute Task 2 (model training and evaluation)
-Execute Task 3A (learning curve plotting)
-Execute Task 3B (vocabulary ablation study)

2) What each part does
load_stopwords(filepath): Loads stopwords from a text file.

convert_text(text): Converts text to lowercase and removes special characters.

handle_negation(tokens): Appends _NEG suffix after encountering "not" or "never" for negation handling.

preprocess(text, stopwords): Cleans the text, tokenizes, handles negation, and removes stopwords.

ngrams_generator(tokens, num): Generates n-grams (like bigrams) from the token list.

task1():
Feature Selection (Task 1)
Processes the training data (train.csv).
Preprocesses text.
Counts unigrams and bigrams.
Selects top 700 unigrams and top 300 bigrams.
Saves the selected features into:
	top_unigrams.txt
	top_bigrams.txt
Prints top 30 unigrams and top 30 bigrams.

extract_features(text, stopwords, top_unigrams, top_bigrams, mode)
-Extracts features from text based on selected unigrams/bigrams.
-mode can be "unigram", "bigram", or "both".

naive_bayes(X, y, vocab)
-Trains the Naive Bayes model.
-Calculates word counts per class (positive/negative) and document counts.

evaluate(y_true, y_pred): Calculates Precision, Recall, and F1 Score.

load_dataset(filepath): 
-Loads dataset (train.csv or test.csv) into texts and labels.
-Label 5-star reviews as 1 (positive), others as 0 (negative).

task2():
Model Training and Evaluation (Task 2)
Loads the top features, trains a Naive Bayes classifier on train.csv.
Predicts on test.csv.
Prints Precision, Recall, and F1 Score.

task3_a():
Learning Curve Plotting (Task 3 Part A)
Trains on 10%, 30%, 50%, 70%, and 100% of the training data.
Evaluates on the full test set.
Plots the F1 Score vs Training Size graph using matplotlib.

task3_b():
Vocabulary Ablation Study (Task 3 Part B)
Trains three different models:
	- Only unigrams
	- Only bigrams
Both unigrams and bigrams
Compares their Precision, Recall, and F1 Score.
Prints a summary table.

main():
Runs all tasks sequentially:
	task1() - Feature selection
	task2() - Train and evaluate
	task3_a() - Learning curve
	task3_b() - Ablation study


