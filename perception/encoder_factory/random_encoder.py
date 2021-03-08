import numpy as np

from perception.core.encoder_factory.base_encoder import BaseEncoder

class RandomEncoder(BaseEncoder):

    def __init__(self, dim):
        self.dim = dim 

    def encode(self, image):

        return np.random.random((1, self.dim))

    def batch_encode(self, images):
        return np.random.random((len(images, self.dim)))
    
    
