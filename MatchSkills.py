import pandas as pd
import numpy as np
import networkx as nx
from fuzzywuzzy import fuzz
from pymongo import MongoClient
p_resume = ["Deep Learning", "Cookie", "Bread", "Wheat"]
client = MongoClient("mongodb://localhost:27017") #host uri
db = client.job_desc_db

all_jobs = db.list_collection_names()
applied_job = 'software_engineer'


def skill_match(p_resume, applied_job, all_jobs):
    print("Checking for", applied_job)
    proc_resume = [i.strip().lower() for i in p_resume]
    flag = "Match Found!"
    new_df = pd.DataFrame()
    for i in db[applied_job].find():
        new_df = new_df.append(i, ignore_index=True)
    G1 = nx.Graph()
    a = np.array(new_df[new_df.columns[1:]].values)
    G1 = nx.from_numpy_matrix(a)
    nx.relabel_nodes(G1, dict(zip(G1.nodes, new_df.columns[1:])), copy = False)
    temp = [j for i in proc_resume for j in G1.nodes if fuzz.ratio(i,j) >= 50]
    temp = list(set(temp))
    k = []
    for i in temp:
        count = 0
        for j in G1.neighbors(i):
            count = count + 1
        k.append(count)
    k_scaled = [(i - min(k))/(max(k) - min(k)) for i in k]
    results = pd.DataFrame()
    results["skills"] = list(temp)
    results["score"] = k_scaled
    results.sort_values(by="score", axis = 0, inplace=True, ascending=False)
    results["combined"] = results["skills"] + ' - ' + results["score"].astype('str')
    score = results.shape[0]/len(G1.nodes)
    print(all_jobs)
    if score < 0.6:
        try: all_jobs.remove(applied_job)
        except: flag = "No Match Found!"
        print(len(all_jobs))
        if len(all_jobs) == 0:
            flag = "No Match Found!"
            score = 0
            results = "None"
            return flag, applied_job, score, results
        if len(all_jobs) > 0:
            return skill_match(proc_resume, all_jobs[0], all_jobs)
    else:
        return flag, applied_job, score, list(results["combined"].head(15))

