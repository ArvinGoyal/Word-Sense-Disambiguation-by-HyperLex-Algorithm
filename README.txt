Word Sense Disambiguation: HyperLex
In this assignment, I took a raw corpus (which will be uploaded here), and run the hyperlex algorithm on it. HyperLex, 
It is an unsupervised WSD algorithm, where the aim is to take all the possible collocations of a word.


The algorithm of HyperLex is as follows:

Tokenize the corpus into sentences, and words. Clean the corpus by removing stopwords (using NLTK)
Define a collocation in a neighborhood. Create pairs of words that occur in the same sentence three words before and three words after. For example, in the sentence: "These people topical notions daily" -> ('topical', 'notions'), ('topical', 'daily') etc.
Rank these collocations based on frequency and create a graph (which words occur with which words the most). The words in the corpus would be the nodes, their cooccurrence defines an edge, and the frequency of the cooccurrence is the weight of that edge
Choose any single focus word, and for all the words in its direct neighbourhood and for words which are two-hops away, remove the most popular nodes, until the graph centered around that focus word splits into subgraphs. 
These words are those which show up in these clusters are those which are most associated with those senses of the word. And voila! Your very own HyperLex implementation. Your assignment is to implement the algorithm described above such that we can input any word in Step 4.

Link to paper: https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.66.6499&rep=rep1&type=pdf
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



Different sense clusters of any three words (power, company, catch) as follows:

power:   ['(president,clause,conditions)', '(program,plant,nuclear)', '(stand,want,one)', '(region,japan,also)']
company: ['(said,million,year)', '(number,double,role)', '(japanese,press,members)', '(tax,flat,financing)']
catch:   ['(glass,says,trading)', '(playing,leading,japanese)']


=====================================================================================================================================================
Reading the file and preparign the training data:

I am reading the file using regex to fetch the words (I am not using POS tag in my code). Then I am removing any stopwords and special characters and 
changing my training data in lower case characters. I have hyper parameter "use_stem" to control if I want to do stemming or not.

=====================================================================================================================================================
Approch:

Step1) For any given target word I am taking all the words that co-occure with it (four word before and four words after) and treat them as nodes. 
Step2) For nodes found in step 1, create a graph within these nodes, to show their co-occurace within these node list. 
Step3) Now created weighted graph b/w its nodes. 0 being highest weight and 1 being lowest weight. Using hyper parameter "min_edge_w"
       I am controlling the miniminum weight b/w two nodes to consider any two nodes in my further processing.
Step4) Using wieghted graph in step 3, prepare a anoher graph which have only required nodes and its edges
Srep5) From graph (formed in step4) fetched the higest degree node and all its nodes connected to it till two hops and from and make a sense 
       cluster. Create a seprate list of sense cluster from sense cluster nodes and remove these selected nodes from main graph (formed in step4)
       As we remove the some nodes from main graph. readjusted the degree/edges of graph's nodes.
Step6) Repeate the step 4 and 5 till in main graph we have node which have degree hhigher the thres hold value/hyper parameter "min_node_degree"
Step7) From list of sense cluster, pick three nodes within a single sense with highest degree and use these three word as sense word.

=====================================================================================================================================================
List of hyperparameter:
I am using below hyper paramenters to tune my program. I have harcoded the values for these hyperparameter in the starting of my program

cmd_prmt = 'N'      # set it to Y if you are running it from command line
use_stem = 'N'      # set to Y if we need to use stemming.
node_co_f = 1       # we can set co-occurance frequencey for any word with root word to consider that word as node.
min_edge_w = 0.9    # what is the minimum edge wieght we need to consider while building the graph. 0 mean nodes are not connected and 1 mean nodes are very tightly connected.
min_node_degree = 2 # While removing sense of a cluster from main graph, minimum dgree of root node.


=====================================================================================================================================================
How to run the Program:

Thier is varailbe "cmd_prmt" which is set to 'Y' assuming that we are ruuning the program from command prompt. If we are running it from 
Jupyter Notebook or any other editor we need to change this vairable to 'N' so that program will prompt to take input file at run time.

This program needs training data (corpus.txt.txt) which has data in specific format (as provided by TA) and I have written regex specific to read 
the data from that perticular format. 
Either we need to keep this file in appropriate directory where we are running this program or need to change our current working directory path 
appropriatly os.chdir("D:\\Arvin\ArtInt\\IIIT PGSSP\\2019-20 Spring\\Assignments\Assignemnt-2\\Corpus")

This Program needs a input file (we need pass this file name as run parameter) which will have a wsingle root word (for which we need to generate 
the different senses clusters)
This program will print/display the different sense of cluster words for given root word on the screen.

