import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ChatBotLogic:
    def __init__(self, data_path):
        self.data = pd.read_excel(data_path)
        self.preprocess_data()
        self.vectorize_data()

    def preprocess_data(self):
        # Filling gaps in the 'message' column
        self.data['message'] = self.data['message'].fillna("No Message")

        # Drop NA rows
        self.data.dropna(inplace=True)
        self.data.reset_index(inplace=True, drop=True)

        # Download stopwords
        nltk.download('stopwords', quiet=True)  # Added quiet=True to suppress download messages
        self.stop_words = stopwords.words('english')

    def vectorize_data(self):
        self.vectorizer = TfidfVectorizer(stop_words=self.stop_words)
        self.vectors = self.vectorizer.fit_transform(self.data['message'])

    def get_response(self, user_input):
        # Tokenize user input
        user_tokens = [word for word in nltk.word_tokenize(user_input) if word.lower() not in self.stop_words]
        user_input_vectorized = self.vectorizer.transform([' '.join(user_tokens)])

        # Calculate cosine similarity
        cosine_similarities = cosine_similarity(user_input_vectorized, self.vectors).flatten()
        best_match_index = cosine_similarities.argmax()

        if cosine_similarities[best_match_index] > 0.2:  # Threshold to filter out low matches
            return self.data.iloc[best_match_index]['message']
        else:
            return "Sorry, I couldn't find a matching response."

# Example Usage (optional):
# if __name__ == "__main__":
#     chatbot = ChatBotLogic('data.xlsx')
#     response = chatbot.get_response('some user input')
#     print(response)
