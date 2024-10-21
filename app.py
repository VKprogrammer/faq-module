from flask import Flask, render_template, request, jsonify
import json
from sentence_transformers import SentenceTransformer, util
# Initialize Flask app
app = Flask(__name__)

# Load FAQ data
with open("faqs.json", "r") as f:
    faqs = json.load(f)

# Preprocess FAQ data
faq_texts = []
faq_list = []  
for category, faq_items in faqs.items():
    for faq in faq_items:
        faq_texts.append(faq["question"])
        faq_list.append(faq)

# Load pre-trained BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight BERT model

# Precompute embeddings for all FAQs
faq_embeddings = model.encode(faq_texts, convert_to_tensor=True)

# Function to search FAQs
def search_faqs(query, top_k=1):
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = util.cos_sim(query_embedding, faq_embeddings)[0]
    top_indices = similarities.topk(top_k).indices.tolist()
    results = [faq_list[index] for index in top_indices]
    return results

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', '')
    results = search_faqs(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
