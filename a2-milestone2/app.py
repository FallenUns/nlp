from flask import Flask, render_template, request, redirect, url_for, jsonify
from sklearn.preprocessing import StandardScaler
from gensim.models.fasttext import load_facebook_vectors
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import joblib
import pandas as pd
import re

app = Flask(__name__)

#Load all of the necessary file
clf = joblib.load('data/logistic_model.pkl')
job_data = pd.read_csv('data/extracted_job_data.csv').to_dict(orient='records')
vocab_dict = {}
with open('data/stopwords_en.txt', 'r') as f:
    stop_words = set(f.read().split())
with open("data/vocab.txt", "r") as f:
    for line in f:
        word, index = line.strip().split(":")
        vocab_dict[word] = int(index)
scaler = joblib.load('data/scaler.pkl')
fasttext_model = load_facebook_vectors('data/crawl-300d-2M-subword.bin')
tfidf_vectorizer = TfidfVectorizer(vocabulary=vocab_dict)

def preprocess_input(desc):
    desc = desc.lower()
    tokens = re.findall(r"[a-zA-Z]+(?:[-'][a-zA-Z]+)?", desc)
    tokens = [token.lower() for token in tokens if len(token) > 2]
    tokens = [token for token in tokens if token not in stop_words]
    tokens = [token for token in tokens if token in vocab_dict]
    return tokens

# Function to convert tokens to vectors
def tokens_to_vector(tokens):
    if len(tokens) == 0:
        return np.zeros(fasttext_model.vector_size)  # or some other default value
    return np.mean([fasttext_model[token] for token in tokens], axis=0)

def prepare_feature_vector(title, description):
    # Preprocess and convert to feature vectors
    title_tokens = preprocess_input(title)
    description_tokens = preprocess_input(description)
    title_vector = tokens_to_vector(title_tokens)
    description_vector = tokens_to_vector(description_tokens)
    
    # Concatenate and scale the vectors
    feature_vector = np.hstack((title_vector, description_vector))
    feature_vector = scaler.transform([feature_vector])
    
    return feature_vector

@app.route('/search', methods=['POST'])
def search_jobs():
    query = request.form.get('searchword').lower()
    search_results = [job for job in job_data if query in job['Title'].lower() or query in job['Description'].lower()]
    return render_template('search_results.html', jobs=search_results)

@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def homepage(page):
    PER_PAGE = 10
    offset = (page - 1) * PER_PAGE
    jobs = job_data[offset:offset + PER_PAGE]
    total_pages = -(-len(job_data) // PER_PAGE)
    return render_template('index.html', jobs=jobs, page=page, total_pages=total_pages)

@app.route('/job/<int:webindex>')
def job_details(webindex):
    job = next(item for item in job_data if item['Webindex'] == webindex)
    return render_template('job_details.html', job=job)

@app.route('/category/<string:category>', defaults={'page': 1})
@app.route('/category/<string:category>/page/<int:page>')
def browse_by_category(category, page):
    PER_PAGE = 10
    filtered_jobs = [job for job in job_data if job['Category'] == category]
    offset = (page - 1) * PER_PAGE
    jobs_to_show = filtered_jobs[offset:offset + PER_PAGE]
    total_pages = -(-len(filtered_jobs) // PER_PAGE)
    return render_template('category.html', jobs=jobs_to_show, category=category, page=page, total_pages=total_pages)

@app.route('/new-job', methods=['GET', 'POST'])
def new_job():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        company = request.form.get('company')
        salary = request.form.get('salary')

        # Generate a new Webindex (you can implement this differently)
        new_webindex = max([job['Webindex'] for job in job_data]) + 1

        # Append new job to job_data
        new_job = {
            'Webindex': new_webindex,
            'Title': title,
            'Description': description,
            'Company': company,
            'Category': category,
            'Salary': salary
        }
        job_data.append(new_job)

        # # Saving the updated job to the csv file
        # updated_df = pd.DataFrame(job_data)
        # updated_df.to_csv('data/extracted_job_data.csv', index=False)

        return redirect(url_for('job_details', webindex=new_webindex))

    return render_template('new_job.html')


@app.route('/predict-category', methods=['POST'])
def predict_category():
    title = request.form.get('title')
    description = request.form.get('description')

    feature_vector = prepare_feature_vector(title, description)
    
    predicted_category = clf.predict(feature_vector)[0]

    return jsonify({'predicted_category': predicted_category})

if __name__ == '__main__':
    app.run()