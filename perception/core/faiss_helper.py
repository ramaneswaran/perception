import os 
import numpy as np 
import faiss
from datetime import datetime



class FaissCore:
    """
    Contains utility function to handle faiss index
    """

    def __init__(self,name: str, store: str, dimension: int, index_type: str ="IndexFlatL2"):
        """
        Constructor for Faiss_core
        """

        try:

            self.index_path = os.path.join(store, name)

            
            self.index = faiss.read_index(self.index_path) if os.path.exists(self.index_path) else faiss.IndexFlatL2(dimension) 


        except Exception as error:
            print(repr(error))
    
    def insert(self, vector):
        """
        Inserts a single vector to the index
        args:  
            vector (np.array): The np.array to be inserted
        returns:
            None
        """

        try:
             
            vector = vector.reshape(1,-1).astype('float32')
            self.index.add(vector)

            index_id = self.index.ntotal

            self.save()

            return index_id

        
        except Exception as error:
            print(repr(error))
    
    def search(self, query, k=1):
        """
        Search for query vector in index
        args:
            query(np.array): Query vector to be searched against index
            k(int): Top k closest records from index will be returned
        return:
            list: List of ids 
        """

        try:
            query = query.reshape(1,-1).astype('float32')
            _, indexes = self.index.search(query, 4)

            return indexes

        except Exception as error:
            print(repr(error))
         
            

    def save(self):
        """
        Saves index with name fname
        The index is stored in index_store
        Args:
            None
        Returns:
            None
        """

        try:
            faiss.write_index(self.index, self.index_path)
            

        except Exception as error:
            print(error)
    
    @property
    def size(self):
        return self.index.ntotal