from abc import ABC, abstractmethod

class BaseEncoder(ABC):

    def encode(self, image):
        """
        Encodes a single image 
        args:
            image (np.array): Image to be encoded
        returns:
            np.array: Encoded vector
        """

        pass 

    def batch_encode(self):
        """
        Encodes a batch of images 
        args:
            images (List[np.array]): List of images to be encoded
        returns:
            List[np.array]: List of encoded vectors
        """
        
        pass 
