### similar to the report_rationalization doc but strictly for graph theory stuff


### IMPORT LIBRARIES
import pandas as pd
import numpy as np 
import csv 
import json
import re
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from scipy.cluster.hierarchy import dendrogram, linkage
import difflib
import scipy.io
import scipy.sparse
import csv


### CHANGE DIRECTORIES
FILENAME = 'report_rationalization.txt'
cols=['username', 'universename', 'reportname', 'sqlstatement', 'queryid']
data = pd.read_table(FILENAME, sep='\t', header=None, names=cols , lineterminator='\n')
data.head()


### REMOVE DUPLICATES
dups = data.groupby(['queryid']).size() #groups unique queryid's together and for each, gives the number of instances that id shows up
dups = dups[dups > 1] #isolate the instances where queryid's show up more than once
summ = sum(dups)
dups = list(dups.index) #now we don't need the count of instances, so save only the queryids as a list of id's that are duplicated
shouldSize = len(data)-summ+len(dups)

for dup_query in dups:
    full_sql_unordered = "" #prepare a string where we will store the concatenated sql statement
    for index, row in data.loc[data['queryid'] == dup_query].iterrows():
        full_sql_unordered = full_sql_unordered + ' ' + row['sqlstatement'] #iterate through the duplicated instances for that queryid and store the sql statment segment
    new = data.loc[data['queryid'] == dup_query].iloc[0] #copy and paste the data so that we have username, date, reportname, etc for our new datapoint
    new['sqlstatement'] = full_sql_unordered #replace the last column (sql statement) with the full unordered sql statement we just made

    #remove old lines from dataframe
    data = data[data['queryid'] != dup_query]

    #add new line to dataframe
    data = data.append(new, ignore_index=True) #RUNTIME ERROR SEEMS TO HAPPEN HERE

isSize = len(data)

# mental check to make sure we deleted all repeated rows
#and replaced them with full sqlstatements
if shouldSize != isSize:
	print "Umm...problem!"
else:
	pass


### CLEANING FOR TOKENS
def filter(statement):
    columns = set(re.findall(r'[a-z_0-9]+\.[a-z_0-9]+\.[a-z_0-9]+', statement))
    columns = ' '.join(columns)
    return columns

data['tokens'] = data['sqlstatement'].apply(lambda x: filter(x))


### TOKENIZE
binVectorizer = CountVectorizer(tokenizer=lambda x: x.split(' '), binary=True)
corpus = binVectorizer.fit_transform(data['tokens'])

# create co-occurence matrix with binary corpus
occur = (corpus.T * corpus)
up = scipy.sparse.triu(occur, k=1) # returns upper tirangular excluding diagonal..sets rest to 0
scipy.io.mmwrite("occurence", occur)

features = binVectorizer.get_feature_names()
features = [x.encode('UTF8') for x in features]
with open("features.txt", "w") as output:
	writer = csv.writer(output, lineterminator='\n')
	for val in features:
		writer.writerow([val])


# check the sparsity of the matrix
print "occurence sparse matrix is", (len(occur.nonzero()[0])/float(occur.shape[0]**2))*100, "percent filled" #available elements
print "'up' sparse matrix only has", len(up.nonzero()[0]), "nonzero elements which is", len(up.nonzero()[0]) == (len(occur.nonzero()[0]) - occur.shape[0])/2
print "So we have", len(up.nonzero()[0]), "edges and", occur.shape[0], "nodes"