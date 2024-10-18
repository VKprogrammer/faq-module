from flask import Flask, render_template, request, jsonify
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load FAQ data from JSON file
with open("faqs.json", "r") as f:
    faq_data = json.load(f)

# Extract questions for vectorization
questions = []
for category in faq_data:  # Iterate through categories in faq_data
    for faq in faq_data[category]:  # Iterate through faqs in each category
        questions.append(faq['question'])

# Initialize TF-IDF Vectorizer and compute question vectors
vectorizer = TfidfVectorizer().fit(questions)
question_vectors = vectorizer.transform(questions)

def find_most_relevant_faq(user_query):
    query_vector = vectorizer.transform([user_query])
    similarities = cosine_similarity(query_vector, question_vectors).flatten()
    best_match_idx = np.argmax(similarities)
    return faq_data[best_match_idx]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    user_query = request.json.get("query")
    if user_query:
        best_faq = find_most_relevant_faq(user_query)
        return jsonify(best_faq)
    return jsonify({"error": "No query provided"}), 400

if __name__ == "__main__":
    app.run(debug=True)
