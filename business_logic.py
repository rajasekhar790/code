import os
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ChatBotLogic:
    def __init__(self):
        # Load and preprocess the data
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.xlsx')
        self.data = pd.read_excel(data_path)

        # Ensure 'message' column exists
        if 'message' not in self.data.columns:
            self.data['message'] = "No Message"

        # Ensure 'action' column exists
        if 'action' not in self.data.columns:
            self.data['action'] = "No action needed"

        self.data.dropna(inplace=True)
        self.data.reset_index(inplace=True, drop=True)

        # Combine all columns into a single 'combined_data' column
        self.data['combined_data'] = self.data[self.data.columns[:]].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)

        # Preprocess the data
        nltk.download('stopwords', quiet=True)
        stop_words = nltk.corpus.stopwords.words('english')
        self.tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.data['combined_data'])

    def get_response(self, user_input):
        # Vectorize the user's input and compute similarity
        user_input_vector = self.tfidf_vectorizer.transform([user_input])
        cosine_similarities = cosine_similarity(user_input_vector, self.tfidf_matrix).flatten()
        related_docs_indices = cosine_similarities.argsort()[:-5:-1]
        
        # If we find a match, return the corresponding message
        if related_docs_indices.size > 0 and cosine_similarities[related_docs_indices[0]] > 0.2:
            return self.data['message'][related_docs_indices[0]]
        else:
            # Return a default response if no match is found
            return "We are working on it."
