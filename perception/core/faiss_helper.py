import os 
import numpy as np 
import faiss

class FaissCore():
    """
    Contains utility function to handle faiss index
    """

    def __init__(self, index_type="IndexFlatL2", dimension):
        """
        Constructor for Faiss_core
        """

        try:
            

            if dimension is None:
                raise Exception("Please specify dimension of vectors to be added in index")

            self.dimension = dimension 

            if index_type == "IndexFlatL2":

                self.index = faiss.IndexFlatL2(dimension)

        except Exception as error:
            print(repr(error))
    
    def insert_record(self, vectors):
        """
        Inserts a single vector to the index
        args:  
            vectors(np.array): The np.array to be inserted
        returns:
            None
        """

        try:

            if vector.shape[1] != self.dimension:
                raise Exception(f'The vector dim should be {self.dimension}, found vector of dimension {vector.shape[1]}')
        
            # Need to update database

            self.index.add(vector)
        
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
            distances, indexes = self.index.search(query, k)

            return indexes

        except Exception as error:
            print(repr(error))
            
         
            

    def save_index(self, fname):
        """
        Saves index with name fname
        The index is stored in index_store
        Args:
            fname (string): Name with which index will be saved
        Returns:
            None
        """

        try:
            index_store_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'index_store')
            index_path = os.path.join(index_store_path, fname)

            self.index.write_disk(self.index, fname)

        except Exception as error:
            print(repr(error))

    def load_saved_index(self, fname):
        """
        Reads a saved index
        The index is usually store in index_store
        Args:
            fname(string): Name of saved index file
        Returns:
            None
        """
        try:
            index_store_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'index_store')
            index_path = os.path.join(index_store_path, fname)

            self.index = faiss.read_index(fname)

        except Exception as error:
            print(repr(error))