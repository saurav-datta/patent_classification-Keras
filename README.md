# W266-Final-Project
Multi-Label Patent Classification with NLP and Neural Networks

We plan on improving on the approach of [this paper](https://res.mdpi.com/def50200a1fc8ccc5cf792a61634f71ed736075024de9cd3f53580e3974e7b8c3869cb1ac14f9a35186e8ca354cef0359e40a64c1b5cfd44ad213c90b4d10caf72f83dc342ac2fc5e121269a960c76c9b2ce4de292c52065365db446022b1a2d4a0d2bca8b4563d79c8001ce69ed62227189389f263037a2bf4db07d1674742378a28b0fd65cbbf67cc5496a130493e396416ed0b2716aded5eed5e8b6f089c6bed2fe3797?filename=&attachment=1) 

## Terminology
International Patent Classification (IPC): 
http://www.wipo.int/classifications/ipc/ipcpub/?notion=scheme&version=20180101&symbol=none&menulang=en&lang=en&viewmode=f&fipcpc=no&showdeleted=yes&indexes=no&headings=yes&notes=yes&direction=o2n&initial=A&cwid=none&tree=no&searchmode=smart

Patent Automatic Classification (PAC): A PAC system is designed for classifying patents into corresponding categories.

continuous bag-of-words (CBOW) algorithm: map words in the patent text into word embeddings

## Data Cleaning and Pre-processing

### Section selection 
- title 
- abstract
- claims
- description

### Labels 
Analysis of the classification labels: 
How many labels (i.e. classes) total do we have (paper has 96)? 
Which level in the Hierarchy will we choose to classify (most papers choose subclasses: e.g. F16L)?
Avg. Number of labels per patent? Paper ~ 1.4
Labels represented in a matrix of 1s and 0s where the rows are the patents and columns all possible labels. 

Y == label matrix 

### Dimensions 
MAX_LEN == maximum length of text for each input section (title, abstract, claims etc.)
- if a section has length less than MAX_LEN, fill in blanks with 0s 
- if a section has length more than MAX_LEN, cut the extra words 

### CBOW for word embeddings

Use CBOW to pre-train our M-CLEF corpora into word embeddings (pick embedding dimensionality (*d*), paper uses 100)

(Paper) Each of the 4 sections will have dimensions *MAX_LEN x d* == 150 x 100

`Triumph`: lets use a smaller max_len for title and abstract 

## Train Val Test Split
training, validation and test datasets, containing 72,532, 18,133, and 2679 mechanical patent documents

## Baseline Models
*CBOW is applied for word embeddings prior to all three models*
- single CNN 
- single LSTM (128 filters)
- single BiLSTM (128 units)

a fully-connected layer with sigmoid activation function was connected to 96 categories from the IPC label matrix

## Hybrid Neural Net Model 

### CNN
- number of filters = 128
- filter size = 3 x 100
- ReLU nonlinearity 

!!! the concatenation strategy is employed after CNN to concatenate the extracted feature maps

### Concatenation Strategies
four versions of HFEM with different concatenation strategies to decide which one yields the best result
- Concatenation (top performer in paper)
- Maximum
- Average
- Summation

**Note**: the paper also considers a `single channel` baseline scenario 

### BiLSTM
The jointed feature maps are the inputs to BiLSTM
128 forward units
128 backward units 

### Fully Connected layer with sigmoid
a fully-connected layer with sigmoid activation is used to calculate the probabilities of 96 IPC labels


## Training parameters
epochs = 40 

## Multi-Class Predictions
Number of target classes = 96 (ours could vary)
 
3 predictions: Top 1 (i.e predicting one IPC label for each patent), Top 5, Top 10 

## Evaluation Metrics
- Precision 
- Recall 
- F1 score 

## Questions that can be explored:

Which section in the patent document has more representative features for classification. 
- use sections separetely as inputs to the same model and check which one performs better