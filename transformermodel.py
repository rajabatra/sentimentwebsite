
import torch
from torch import nn
import math
from tokenizers import decoders, models, normalizers, pre_tokenizers, processors, trainers, Tokenizer
import torch.nn.functional as F
from torch.nn.utils.rnn import pad_sequence





from torch.nn import TransformerEncoder, TransformerEncoderLayer

class TransformerClassifier(nn.Module):
    def __init__(self, vocab_size, d_model, nhead, hiddendim, numlayers, num_classes=2, dropout = 0.1, max_len=250):
        super(TransformerClassifier, self).__init__()
        # Embedding layer
        self.embedding = nn.Embedding(vocab_size, d_model)

        #positional encoding
        self.positional_encoding = PositionalEncoding(d_model, max_len=max_len)

        # Transformer layer
        transformer_layer = TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=hiddendim, dropout=dropout)
        self.transformer = TransformerEncoder(transformer_layer, num_layers=numlayers)
        # Output layer
        self.fc = nn.Linear(d_model, num_classes)

    def forward(self, x):
        x = self.embedding(x)
        x = self.positional_encoding(x)
        x = self.transformer(x)
        x = torch.mean(x, dim=1)

        x = self.fc(x)
        return x

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=50):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=0.1)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * -(math.log(10000.0) / d_model))
        pe = torch.zeros(1, max_len, d_model)
        pe[0, :, 0::2] = torch.sin(position * div_term)
        pe[0, :, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:, :x.size(1)].detach()
        return self.dropout(x)







def analyze_sentiment(headline):
    tokenizer = Tokenizer.from_file("customtokenizer.json")
    model = torch.load('transformermodelsubword.pth', map_location=torch.device('cpu'))
    model.eval()  # Set the model to evaluation mode
    tokenizer = tokenizer
    # Tokenize the headline using your custom tokenizer
    words = tokenizer.encode(headline).tokens

    # Convert words to numerical indices
    numerical_indices = [tokenizer.token_to_id(word) for word in words]
    numerical_indices =torch.as_tensor(numerical_indices, dtype=torch.long).unsqueeze(0) 
  
    #print(numerical_indices.shape)
    

    # Perform sentiment analysis using your PyTorch model
    with torch.no_grad():
        sequence = torch.randint(0, 25000, (5,))  # Replace 250 with your desired sequence length
       # print(sequence.shape)
        # Ensure the input sequence has the correct shape
        sequence = sequence.unsqueeze(0)  
        #print(sequence.shape)
        outputs = model(numerical_indices)
        #output = model(numerical_indices.unsqueeze(0))  # Assuming your model takes a batch of sequences

    # Extract sentiment score or class from the model output
    print(outputs)
    _ , sentiment_score = torch.max(outputs, 1)  # Replace with your logic based on the model output format
    print(sentiment_score.item())
    if sentiment_score == 1:
        return 1
    return 0
