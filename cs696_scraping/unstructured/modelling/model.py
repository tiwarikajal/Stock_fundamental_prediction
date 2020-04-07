from transformers import BertTokenizer, BertModel, BertConfig
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class UnStructuredModel:
    
    def __init__(self, model_name, max_length, stride):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.max_length = max_length
        self.stride = stride
        if model_name == 'bert-base-uncased':
            configuration = BertConfig()
            self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
            self.model = BertModel(configuration).from_pretrained(self.model_name)
            self.model.to(device)
            self.model.eval()
            
        

    def padTokens(self, tokens):
        if len(tokens)<self.max_length:
            tokens = tokens + ["[PAD]" for i in range(self.max_length - len(tokens))]
        return tokens

    def getEmbedding(self, text, if_pool=True, pooling_type="mean", batchsize = 1):
        tokens = self.tokenizer.tokenize(text)
        tokenized_array = self.tokenizeText(tokens)
        embeddingTensorsList = [] 
        print(len(tokenized_array))
        if len(tokenized_array)>batchsize:
            for i in range(0, len(tokenized_array), batchsize):
                current_tokens = tokenized_array[i:min(i+batchsize,len(tokenized_array))]
                token_ids = torch.tensor(current_tokens).to(device)
                seg_ids=[[0 for _ in range(len(tokenized_array[0]))] for _ in range(len(current_tokens))]
                seg_ids   = torch.tensor(seg_ids).to(device)
                hidden_reps, cls_head = self.model(token_ids, token_type_ids = seg_ids)
                embeddingTensorsList.append(cls_head)
            embedding = torch.cat(embeddingTensorsList, dim=0)
        else:
            token_ids = torch.tensor(tokenized_array).to(device)
            seg_ids=[[0 for _ in range(len(tokenized_array[0]))] for _ in range(len(tokenized_array))]
            seg_ids   = torch.tensor(seg_ids).to(device)
            hidden_reps, cls_head = self.model(token_ids, token_type_ids = seg_ids)
            embedding = cls_head
        if if_pool and pooling_type=="mean":
            embedding = torch.mean(embedding, dim=0)
        return embedding

    def tokenizeText(self, tokens):
        tokens_array = []
        #window_movement_tokens =  max_length - stride 
        for i in range(0, len(tokens), self.stride):
            if i+self.max_length<len(tokens):
                curr_tokens = ["CLS"] + tokens[i:i+self.max_length] + ["SEP"]
            else:
                padded_tokens = self.padTokens(tokens[i:i+self.max_length])
                curr_tokens = ["CLS"] + padded_tokens + ["SEP"]
            curr_tokens = self.tokenizer.convert_tokens_to_ids(curr_tokens)
            tokens_array.append(curr_tokens)
        return tokens_array    
