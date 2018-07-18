# W266-Final-Project
Multi-Label Patent Classification with NLP and Neural Networks

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