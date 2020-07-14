
# coding: utf-8

# In[1]:


import os
import re
from collections import defaultdict, Counter
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
ps = PorterStemmer()

import sys


# In[2]:


#Hyper Parameters:

cmd_prmt = 'Y'      # set it to Y if you are running it from command line
use_stem = 'N'      # set to Y if we need to use stemming.
node_co_f = 1       # we can set co-occurance frequencey for any word with root word to consider that word as node.
min_edge_w = 0.9    # what is the minimum edge wieght we need to consider while building the graph. 0 mean nodes are not connected and 1 mean nodes are very tightly connected.
min_node_degree = 2 # While removing sense of a cluster from main graph, minimum dgree of root node.


# In[14]:


#root_word = input("Provide the word for which you are looking for different sences:")

if cmd_prmt =='Y':
    input_file_name = sys.argv[1]
else:
    os.chdir("D:\\Arvin\ArtInt\\IIIT PGSSP\\2019-20 Spring\\Assignments\Assignemnt-2\\Corpus") 
    input_file_name = input("Provide the name on input file having the Root Word for which we need to find multiple senses:")

i_file = open(input_file_name,"r")
input_file = i_file.readlines()
i_file.close()

O = []                # O: list of observations
for i in range (len(input_file)):
    if i == 0:
        root_word = input_file[i].lower()
if use_stem == 'Y':
    rootword = ps.stem(root_word)    


# In[96]:


#nltk.download('stopwords')
#print(stopwords.words('english'))


# In[15]:


file = open('corpus.txt',"r")
corpus = file.readlines()
file.close()

# (?<=\(')((\w[.-])*\w?)+(?=')     - Look Behind: ('  followed by zero and more word [.-] followed by zero or more word Look ahead '
# (?<=\(')[\w\s\.\-]+(?=')          - Look Behind: ('  followed by zero and more word including [.-] Look ahead '

fetch_word_re = re.compile("(?<=\(')[\w\s\-]+(?=')")
cust_stopword = stopwords.words('english')
#cust_stopword = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
text = []
for i in range(len(corpus)):
    sentence_temp = re.findall(fetch_word_re, corpus[i])
    #sentence_temp = [word for word in sentence_temp if not word.lower() in stopwords.words('english')]
    sentence_temp = [word for word in sentence_temp if not word.lower() in cust_stopword]
    text.append(sentence_temp)

def clean_non_alpha(text):
    non_alpha_re = re.compile("[\.\-0-9]+")
    #remove_extra_spance = re.compile("[  ]+")
    remove_extra_spance = re.compile("(  )+")
    clean_text = []

    for sent in text:
        clean_sent = []
        for w in sent:
            w = non_alpha_re.sub(' ', w)
            w = remove_extra_spance.sub(' ', w)
            w = w.lower()
            if use_stem == 'Y':
                w = ps.stem(w)
            w = w.split()
            clean_sent.extend (w)
            clean_sent = [word for word in clean_sent if not word in cust_stopword]
            
            
        clean_text.append(clean_sent)
    return clean_text

clean_text = clean_non_alpha(text)


# In[16]:


def get_node_list():
    node_lst = []
    node_root_count   = defaultdict(lambda: 0)
    for sentence in clean_text:
        prev_w1 = ''
        prev_w2 = ''
        prev_w3 = ''
        prev_w4 = ''
        next_w_node = 0
        
        for w in sentence:
            if next_w_node > 0:
                if w != root_word and len(w)>0:
                    #node_lst.append(w)
                    node_root_count[w] +=1
                next_w_node = next_w_node-1
                
            if w == root_word:
                next_w_node = 4                            # if we need to provide how many forward word we need to take 
                if prev_w1 != root_word and len(prev_w1)>0:
                    #node_lst.append(prev_w1)
                    node_root_count[prev_w1] +=1
                #"""
                if prev_w2 != root_word and len(prev_w2)>0:
                    #node_lst.append(prev_w2)
                    node_root_count[prev_w2] +=1
                #"""
                if prev_w3 != root_word and len(prev_w3)>0:
                    #node_lst.append(prev_w3)
                    node_root_count[prev_w3] +=1
                #"""   
                if prev_w4 != root_word and len(prev_w4)>0:
                    #node_lst.append(prev_w3)
                    node_root_count[prev_w4] +=1
                #"""                   
            prev_w4 = prev_w3
            prev_w3 = prev_w2
            prev_w2 = prev_w1
            prev_w1 = w      
    
        
    for node in list(node_root_count.keys()):
        if node_root_count [node]>=node_co_f:
            node_lst.append(node)
    
    node_lst =list(set(node_lst))        
    return node_lst


def count_and_co_occurance():
    
    for sentence in clean_text:
        prev_w1 = ''
        prev_w2 = ''
        prev_w3 = ''
        # next_node_window = 0           #we don't need to see both side of current node.  We taking three back words to check co-occurance  as in string 'abcd'  occurance (ad) = occurance (da)
        for w in sentence:
            for node1 in node_list:
                if w == node1:
                    w_count[w] += 1
                    
                    for node2 in node_list:
                        if prev_w1 == node2:
                            if node1 <= node2:
                                co_occur[node1][node2] += 1
                            else:
                                co_occur[node2][node1] += 1
                        
                        if prev_w2 == node2:
                            if node1 <= node2:
                                co_occur[node1][node2] += 1
                            else:
                                co_occur[node2][node1] += 1                                
                                
                        if prev_w3 == node2:
                            if node1 <= node2:
                                co_occur[node1][node2] += 1
                            else:
                                co_occur[node2][node1] += 1                                
                        """ 
                        we can reduce the number of hops while checking co-occur count
                        """
            prev_w3 = prev_w2
            prev_w2 = prev_w1
            prev_w1 = w


# In[17]:


co_occur  = defaultdict(lambda: defaultdict(lambda: 0))
w_count   = defaultdict(lambda: 0)

node_list = get_node_list()
count_and_co_occurance ()          # co_occur dictionary have only one entry for two words (small word first level key and then second word).


# In[18]:


#print('Root word is: ',root_word)
#print('There are the',len(node_list),  'nodes for provided root word:\n')
#print(node_list)


# In[19]:


def edge_weight():
    for node1 in list(co_occur.keys()):
        for node2 in list(co_occur[node1].keys()):
            edge_w [node1][node2] = 1
            if w_count[node1] <= w_count[node2]:
                if w_count[node1] >=5:                        # it prevent devide by zero error and also make sure word occur atleast 10 times
                    edge_w [node1][node2] = (1-(co_occur[node1][node2]/w_count[node1]))
                    #print (node1,"-", node2, "weight: ", edge_w [node1][node2])
            else:
                if w_count[node2] >=5:                        # it prevent devide by zero error and also make sure word occur atleast 10 times
                    edge_w [node1][node2] = (1-(co_occur[node1][node2]/w_count[node2])) 
                    #print (node1,"-", node2, "weight: ", edge_w [node1][node2])
            


# In[20]:


def create_graph():
    for node1 in list(edge_w.keys()):
        for node2 in list(edge_w[node1].keys()):
            if edge_w[node1][node2] < min_edge_w:
                graph[node1].append(node2)
                graph[node2].append(node1)
            
def highest_dgree_node():
    hd_node = 'blank'
    hd = 1
    for node in list(graph.keys()):
        if len(graph[node]) > hd:
            hd_node = node
            hd = len(graph[node])
    return hd_node, hd

def node_list_two_hopes(hd_node):
    list1 = [hd_node]
    list2 = graph[hd_node]
    list3 = []
    for node in list2:
        list3.extend(graph[node])
    remove_nodes = list1 + list2 +list3
    return list(set(remove_nodes))
    
def nodes_in_graph(graph):
    node_lst = []
    for node in list(graph.keys()):
        node_lst.append(node)
    return set(node_lst)
        
def cut_graph(graph,sense,sense_graph_list):
    graph_remain = defaultdict(lambda: [])
    g_nodes = nodes_in_graph (graph)
    remain_nodes = list(g_nodes - set(remove_nodes))
    
    for node in list(graph.keys()):
        if node in remain_nodes:
            edge_nodes = []
            for edg_nd in graph[node]:
                if edg_nd in remain_nodes:
                    edge_nodes.append(edg_nd)
            graph_remain[node]=edge_nodes
        
        if node in remove_nodes:
            edge_nodes = []
            for edg_nd in graph[node]:
                if edg_nd in remove_nodes:
                    edge_nodes.append(edg_nd)
            sense_graph_list[sense][node]=edge_nodes
    
    return graph_remain,sense_graph_list
    


# In[21]:


edge_w   = defaultdict(lambda: defaultdict(lambda: 0))
graph = defaultdict(lambda: [])
sense_graph_list = defaultdict(lambda: defaultdict(lambda: []))
sense = 0

edge_weight()
edge_w_backup = edge_w

create_graph()

#print (graph['talk'])
hd_node, hd = highest_dgree_node()
while True:
    if hd>= min_node_degree:
        #print('Sense number:', sense, '  Root node:',hd_node, '  Root node degree:', hd)
        remove_nodes = node_list_two_hopes(hd_node)
        #print(remove_nodes,'\n')
        graph,sense_graph_list = cut_graph(graph,sense,sense_graph_list)
        
        sense +=1
        hd_node, hd = highest_dgree_node()
    else:
        break


# In[24]:


print("Senses for Root Word",root_word,"is:" )
list_senses = []
for s in range(sense):
    deg1_w = ''
    deg1=0
    deg2_w = ''
    deg2=0
    deg3_w = ''
    deg3=0    
    
    #rint ("List for Sense ", s, ":")
    sense_word_lst = []
    for node1 in list(sense_graph_list[s].keys()):
        sense_word_lst.append(node1)
        for node2 in sense_graph_list[s][node1]:
            sense_word_lst.append(node2)
    sense_word_lst = list(set(sense_word_lst))
    
    for sw in sense_word_lst:
        if len(sense_graph_list[s][sw]) > deg1:
            deg1 = len(sense_graph_list[s][sw])
            deg1_w = sw
        else: 
            if len(sense_graph_list[s][sw]) > deg2:
                deg2 = len(sense_graph_list[s][sw])
                deg2_w = sw
            else: 
                if len(sense_graph_list[s][sw]) > deg3:
                    deg3 = len(sense_graph_list[s][sw])
                    deg3_w = sw
    sense_cluster = "(" + deg1_w + "," + deg2_w + "," + deg3_w + ")"
    #print (sense_cluster)
    list_senses.append(sense_cluster)
                    
            
print (list_senses)

