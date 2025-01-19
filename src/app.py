# Copyright (c) 2025, Your Name
# Licensed under the MIT License. See LICENSE for details.

"""
Description
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from collections import defaultdict

from lit import lit_list


app = Flask(__name__)


articles_db = {}  # This will hold article data by ID
votes_db = defaultdict(lambda: {'upvotes': 0, 'downvotes': 0})  # Tracks votes for each article

def research_papers():
    query = "(ISO AND 8800) OR (AI AND DevOps) OR (AI AND Safety) OR (Deep AND LEARNING AND Safety) OR (AI AND (Standart OR Norm)) "
    
    print(f" Searching for {query}")
    return lit_list(query)

@app.route('/')
def index():
    # By default, show all papers
    papers = research_papers()
    for article in papers:
        if article.id not in articles_db:
            articles_db[article.id] = {
                'title': article.title,
                'date': article.date,
                'summary': article.summary,
                'url': article.url,
                'id': article.id
            }
            
    articles_with_votes = [
        {
            **articles_db[article.id],
            'upvotes': votes_db[article.id]['upvotes'],
            'downvotes': votes_db[article.id]['downvotes'],
            'score': votes_db[article.id]['upvotes'] - votes_db[article.id]['downvotes']
        }
        for article in papers
    ]
 
    return render_template('index.html', papers=articles_with_votes, filter_days=None)

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    article_title = data.get('article_title')
    vote_type = data.get('vote_type')

    if article_title not in articles_db:
        return jsonify({'error': 'Article not found'}), 404

    if vote_type == 'upvote':
        votes_db[article_title]['upvotes'] += 1
    elif vote_type == 'downvote':
        votes_db[article_title]['downvotes'] += 1
    else:
        return jsonify({'error': 'Invalid vote type'}), 400

    # Return the updated score
    score = votes_db[article_title]['upvotes'] - votes_db[article_title]['downvotes']
    return jsonify({'score': score})


@app.route('/filter', methods=['POST'])
def filter_papers():
    # Get the filter value from the form
    filter_days = int(request.form['filter_days'])
    papers = research_papers()
    cutoff_date = datetime.now() - timedelta(days=filter_days)
    filtered_papers = [paper for paper in papers if paper.date.astimezone(None) >= cutoff_date.astimezone(None)]
    
    for article in filtered_papers:
        if article.id not in articles_db:
            articles_db[article.id] = {
                'title': article.title,
                'date': article.date,
                'summary': article.summary,
                'url': article.url,
                'id': article.id
            }
            
    articles_with_votes = [
        {
            **articles_db[article.id],
            'upvotes': votes_db[article.id]['upvotes'],
            'downvotes': votes_db[article.id]['downvotes'],
            'score': votes_db[article.id]['upvotes'] - votes_db[article.id]['downvotes']
        }
        for article in filtered_papers
    ]

    return render_template('index.html', papers=articles_with_votes, filter_days=filter_days)



if __name__ == '__main__':
    app.run(debug=True)