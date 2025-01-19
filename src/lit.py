# Copyright (c) 2025, Your Name
# Licensed under the MIT License. See LICENSE for details.

"""
Description
"""

import arxiv 
from datetime import datetime, timedelta

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class Paper:
    def __init__(self, title, date, summary, url, authors):
        self.title = title
        self.date = date
        self.summary = summary
        self.url = url
        self.id = url.split('/')[-1]
        self.authors = authors

def is_within_last_week(given_date):
    # Get the current date
    current_date = datetime.now()
    
    # Calculate the date 7 days ago
    last_week = current_date - timedelta(days=7)
    
    # Check if the given date is between last week and today

    return last_week.astimezone(None) <= given_date.astimezone(None) <= current_date.astimezone(None)



def lit_list(query):
    # Construct the default API client.
    client = arxiv.Client()

    # Search for the 10 most recent articles matching the keyword "quantum."
    search = arxiv.Search(
    query = query,
    max_results = 20,
    sort_by = arxiv.SortCriterion.SubmittedDate
    )

    papers = []

    # `results` is a generator; you can iterate over its elements one by one...
    for r in client.results(search):
        author_string=  "; ".join(author.name for author in r.authors)
        papers.append(Paper(title=r.title, authors=author_string, date=r.published, summary=r.summary, url=str(r)))
        
    return papers