import pandas as pd
import numpy as np
import networkx as nx
from bs4 import BeautifulSoup
import requests
import re
from progressbar import ProgressBar
import matplotlib.pyplot as plt
# homePage = "https://relatedwords.io/deep-learning"
resume = [["deep learning", "machine learning", "deep understanding", "opportunity", "reinforcement learning applications", "Prior experience", "hands-on experience", "Python", "cybersecurity", "Kubernetes", "Work-life flexibility", "medical devices", "application development", "Scala programing", "career development", "Docker containers", "computer networking", "IOT network security", "high-fidelity synthetic network flows", "behavioral anomaly detection", "office space", "Spark Streaming", "Postgres databases", "stack", "mid-town NYC", "Kafka", "general algorithm design", "Unique perks", "device fingerprinting", "optimization", "multi-disciplinary team", "wide range of technologies", "Growth opportunities", "research", "Competitive intern salary", "collaborative environment", "contributions", "orchestration", "Haves", "Benefits", "Location", "gear", "productivity", "Skills"],
          ["Data Manipulation", "knowledge of Machine Learning", "data analysis", "modeling team", "Artificial intelligence applications", "new data sources", "Artificial Intelligence techniques", "Model Validation", "Model Estimation", "Primary Duties", "team environment", "Modeling Research Knowledge Job Specifications", "Strong analytical background", "intern's primary function", "general operational needs", "Responsibilities", "transactions", "recommendations", "SAS", "python", "ability", "Abilities", "Expert", "econometric understanding", "Excel", "sound business judgment", "Skills", "willingness", "relevant findings", "information"],
          ["data tools", "data quality", "data access", "contextual data", "data modeling", "data-driven development", "data driven solutions", "real-time data pipelines", "data processing frameworks", "data storage techniques", "large scale data infrastructure", "high volume heterogeneous data", "complex data-related problems", "music", "agile software processes", "functional agile teams", "insight tools", "software engineers", "millions of artists", "product features", "new product objectives", "user behaviors", "acoustical analysis", "revenue streams", "Scalding", "Spark", "Storm", "stakeholders", "Scio", "distributed systems", "diverse datasets available", "broad range of mobile", "digital media experiences", "signals", "reliability", "leadership opportunities", "active users", "large-scale batch", "continuous integration", "best practices", "delivery", "Hadoop", "BigTable", "connected platforms", "learning", "experts", "tooling", "Google Cloud Platform", "responsible experimentation", "way people", "single day", "Help", "optimization", "Cassandra", "value of partnership", "Title"],
          ["test software", "software platforms", "Proficiency", "software developer", "software modules", "software installation support", "automated deployment software", "purpose of conveying software design decisions", "understanding of agile software methodologies", "system administration of Linux", "database administration tasks", "Unix system administration activities", "specific technologies", "Desired Experience", "Practical experience", "Unix systems", "DevOps technologies", "automated test", "database engineering", "candidates", "web-based technologies", "programming languages", "scripting languages", "development team", "team environment", "Specific duties", "cloud technology", "familiarity", "portals", "user interfaces", "resource utilization", "distributed architectures", "year of start date", "databases", "various sources", "performance standards", "proper operation of hardware", "wide variety of applications", "configuration of commercial products", "Javascript", "stability", "direct customer interaction", "MongoDB", "PostGres", "integrator", "Puppet", "Chef", "Docker", "Oracle", "diverse dynamic workforce", "Security Clearance", "position", "experts", "C++", "Perl", "implementation tools", "Python", "C#", "Scrum", "Citizenship status"]
          ]
collec_nm = ["data_scientist", "quantitative_analyst", "data_engineer", "software_engineer"]
def clean_html(html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '$', str(html))
    return cleantext

def key_words_extract(homePage, max_num):
    openPage = requests.get(homePage)
    soup = BeautifulSoup(openPage.content, 'lxml')
    keywords = []
    temp_0 = soup.find(id='terms-list')
    try: temp_01 = len(list(temp_0))
    except:
        temp_01 = 0
    if temp_01 > 0:
        temp = temp_0.find_all('a')
        count = 0
        for i in temp:
            count = count + 1
            keywords.append(clean_html(i).replace('$',''))
            if count==max_num :
                break
    return keywords

def create_link(word):
    return "https://relatedwords.io/"+word.replace(' ', '-')

def create_edges(resume, max_key=10):
    bar = ProgressBar()
    edges = []
    for i in bar(resume):
        keywords = key_words_extract(create_link(i), max_num = max_key)
        if len(keywords) > 0:
            for j in keywords:
                edges.append([i, j.replace('.','')])
        else:
            continue
    return edges

# resume = [i.lower() for i in resume if len(i) > 0]
# # resume
# edges = create_edges(resume, max_key=10)
# G = nx.Graph()
# G.add_edges_from(edges)
#
# plt.figure(figsize = (20,16))
# plt.axis("off")
# spring_pos = nx.spring_layout(G)
# values = np.random.randint(0,255, size=len(G.nodes()))
# nx.draw_networkx(G, pos = spring_pos, cmap = plt.get_cmap("jet"), node_color = values, node_size = 45,
#                     alpha = 0.75, with_labels = True, edge_color='grey')
# plt.show()
#
# mat = nx.adjacency_matrix(G)
# df = pd.DataFrame(mat.todense(), columns=G.nodes)
# df.head()
# df.to_json

#### push data to MongoDB

import pymongo
from pymongo import MongoClient
import json
# client = MongoClient('localhost', 27017)
# client.drop_database('job_desc_db')
# db = client['job_desc_db']
# db
# db_cm = db[collec_nm]
# db_cm
# data_json = json.loads(df.to_json(orient='records'))
# x = db_cm.insert(data_json)
# len(x)

def db_push(resume, db_name, collec_nm):
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    print("Inserting data into ", collec_nm)
    resume = [i.lower() for i in resume if len(i) > 0]
    # resume
    edges = create_edges(resume, max_key=10)
    G = nx.Graph()
    G.add_edges_from(edges)
    mat = nx.adjacency_matrix(G)
    df = pd.DataFrame(mat.todense(), columns=G.nodes)
    db_cm = db[collec_nm]
    data_json = json.loads(df.to_json(orient='records'))
    id = db_cm.insert(data_json)
    return str(len(id))+" records inserted"

db_name = 'job_desc_db'
for i in range(0, len(collec_nm)):
    db_push(resume[i], db_name, collec_nm[i])

