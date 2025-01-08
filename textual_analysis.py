import pandas as pd
import os
import nltk
import textstat
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob.en import sentiment


def textual_anal():
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger_eng')
    nltk.download('wordnet')


    stop_words = stopwords.words('english')
    lemma = nltk.WordNetLemmatizer()


    def clean_text(text):
        '''Purpose: Cleans the input text.
        Parameters: text - the text which needs to be cleaned.
	                stop-words – list of words which are to be cleaned from the text.
        Returns cleaned text
        '''
        words = nltk.word_tokenize(text.lower())
        cleaned_words = [word for word in words if word not in stop_words and word.isalpha()]
        lemmatize = [lemma.lemmatize(w) for w in cleaned_words]
        return ' '.join(lemmatize)


    def analyze_text(text):
        '''This function performs various types of textual analysis on the cleaned article text:
        Parameters: text – text on which textual analysis is to be performed
                    stop_words – to clean text
                    positive_words- set of positive words
                    negative_words – set of negative words
        Returns a dictionary with all the computed metrics for the article.
        '''
        cleaned_text = clean_text(text)

        # Sentiment analysis
        words = cleaned_text.split()
        blob = TextBlob(text)

        polarity_score = blob.sentiment.polarity
        subjectivity_score = blob.sentiment.subjectivity

        if polarity_score > 0:
            sentiment = 'Positive'
        elif polarity_score < 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'

        positive_score = max(0, polarity_score)
        negative_score = max(0, -polarity_score)

        #word_count on cleaned text
        word_count = len(words)

        # Tokenize text into sentences and words
        sentences = nltk.sent_tokenize(text)
        words = nltk.word_tokenize(text)

        # Average sentence length
        avg_sentence_length = word_count / len(sentences) if len(sentences) > 0 else 0

        # Count complex words (words with 3 or more syllables)
        complex_word_count = sum(1 for word in words if textstat.syllable_count(word) > 2)

        # Percentage of complex words
        percentage_complex_words = (complex_word_count / word_count) * 100 if word_count > 0 else 0

        # Fog Index
        fog_index = textstat.gunning_fog(text)

        # Syllables per word
        syllables_per_word = sum(textstat.syllable_count(word) for word in words) / word_count if word_count > 0 else 0

        # Count personal pronouns
        personal_pronouns = sum(1 for word, tag in nltk.pos_tag(words) if tag in ["PRP", "PRP$"])

        # Average word length
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0

        return {
            "sentiment": sentiment,
            "positive_score": positive_score,
            "negative_score": negative_score,
            "polarity_score": polarity_score,
            "subjectivity_score": subjectivity_score,
            "avg_sentence_length": avg_sentence_length,
            "percentage_complex_words": percentage_complex_words,
            "fog_index": fog_index,
            "complex_word_count": complex_word_count,
            "word_count": word_count,
            "syllables_per_word": syllables_per_word,
            "personal_pronouns": personal_pronouns,
            "avg_word_length": avg_word_length
        }


    def process_articles(articles_dir):
        '''Purpose: Processes all articles stored in the articles_dir and creates an excel file storing the result.
        Parameters: articles_dir – directory containing all the files on which textual analysis needs to be  performed.

        Returns None
        '''
        results = []

        for filename in os.listdir(articles_dir):
            article_title = filename.split('.')[0]
            article_file = os.path.join(articles_dir, filename)

            with open(article_file, 'r', encoding='utf-8') as f:
                article_text = f.read()

            analysis = analyze_text(article_text)

            result = {
                "ARTICLE_TITLE": article_title,
                "SENTIMENT": analysis["sentiment"],
                "POSITIVE SCORE": analysis["positive_score"],
                "NEGATIVE SCORE": analysis["negative_score"],
                "POLARITY SCORE": analysis["polarity_score"],
                "SUBJECTIVITY SCORE": analysis["subjectivity_score"],
                "AVG SENTENCE LENGTH": analysis["avg_sentence_length"],
                "PERCENTAGE OF COMPLEX WORDS": analysis["percentage_complex_words"],
                "FOG INDEX": analysis["fog_index"],
                "AVG NUMBER OF WORDS PER SENTENCE": analysis["avg_sentence_length"],
                "COMPLEX WORD COUNT": analysis["complex_word_count"],
                "WORD COUNT": analysis["word_count"],
                "SYLLABLE PER WORD": analysis["syllables_per_word"],
                "PERSONAL PRONOUNS": analysis["personal_pronouns"],
                "AVG WORD LENGTH": analysis["avg_word_length"]
            }
            results.append(result)

        df = pd.DataFrame(results)
        df.to_excel("articles_analysis.xlsx")

    articles_directory = "articles"

    process_articles(articles_directory)
