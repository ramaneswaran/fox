import numpy as np
import networkx as nx

class TextRank:
    '''
    This class provides functions to use TextRank summarization algorithm
    '''
    
    def __init__(self, model):
        self.model = model
    
    def get_sents(self, text):
        '''
        This functions splits text into sentences
        '''
        sents = self.model.sentencize(text)
        return sents
    
    def get_sim(self, text1, text2):
        '''
        This functions gets similarity between texts
        '''
    
        return self.model.sent_sim(text1, text2)
    
    def build_sim_mat(self, sents):
        '''
        This function builds a similarity matrix
        '''
        
        size = len(sents)
        sim_mat = np.zeros((size, size))
        
        for idx1 in range(size):
            for idx2 in range(size):
                if idx1==idx2:
                    continue
                sim_mat[idx1][idx2] = self.get_sim(sents[idx1], sents[idx2])
        
        return sim_mat
    
    def build_graph(self, sim_mat):
        '''
        This function builds sent sim graph
        '''
        
        sim_graph = nx.from_numpy_array(sim_mat)
        return sim_graph
    
    def get_page_rank(self, sim_graph):
        '''
        This function computes page rank
        '''
        
        scores = nx.pagerank(sim_graph)
        return scores
    
    def summarize(self, text, n_sents = 1):
        '''
        This function summarizer the text
        '''
        
        sents = self.get_sents(text)
        sim_mat = self.build_sim_mat(sents)
        sim_graph = self.build_graph(sim_mat)
        scores = self.get_page_rank(sim_graph)
        ranked_sent = sorted(((scores[i], s) for i,s in enumerate(sents)), reverse=True)
        
        summary = ''
        for idx in range(n_sents):
            summary+=ranked_sent[idx][1]
            
        return summary
    
    def top_sentences(self, text, n_sents = 1):
        '''
        This function returns top ranked sentences
        '''
        sents = self.get_sents(text)
        sim_mat = self.build_sim_mat(sents)
        sim_graph = self.build_graph(sim_mat)
        scores = self.get_page_rank(sim_graph)
        ranked_sent = sorted(((scores[i], s) for i,s in enumerate(sents)), reverse=True)
        
        if n_sents > len(ranked_sent):
            n_sents = len(ranked_sent)
        
        result = []
        for idx in range(n_sents):
            result.append(ranked_sent[idx][1])
        
        return result