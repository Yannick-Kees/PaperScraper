# Copyright (c) 2025, Your Name
# Licensed under the MIT License. See LICENSE for details.

"""
Description
"""

from flask import Flask, render_template, request
from datetime import datetime, timedelta

from lit import lit_list


app = Flask(__name__)


def research_papers():
    query = "(ISO AND 8800) OR (AI AND DevOps) OR (AI AND Safety) OR (Deep AND LEARNING AND Safety) OR (AI AND (Standart OR Norm)) "
    
    print(f" Searching for {query}")
    return lit_list(query)

@app.route('/')
def index():
    # By default, show all papers
    papers = research_papers()
    return render_template('index.html', papers=papers, filter_days=None)

@app.route('/filter', methods=['POST'])
def filter_papers():
    # Get the filter value from the form
    filter_days = int(request.form['filter_days'])
    papers = research_papers()
    cutoff_date = datetime.now() - timedelta(days=filter_days)
    filtered_papers = [paper for paper in papers if paper.date.astimezone(None) >= cutoff_date.astimezone(None)]
    return render_template('index.html', papers=filtered_papers, filter_days=filter_days)

if __name__ == '__main__':
    app.run(debug=True)