import torch 
import torch.nn as nn
from torchvision.models import vgg16
from torchvision.transforms import transforms
from perception.encoders.base import BaseEncoder

class VGGEncoder(BaseEncoder):

    def __init__(self):
        self.setup()

    def encode(self, image):
        """
        Encodes an image and returns its feature vector
        Args:
            image (np.ndarray): The image to be encoded
        Returns:
            np.ndarray: The feature vector of image
        """

        image = self.transform(image) 
        image = image.unsqueeze(0)
        feature = self.encoder(image).squeeze(0)

        return feature.detach().cpu().numpy() if feature.requires_grad else feature.cpu().numpy()
    
    def setup(self):
        
        vgg_model = vgg16(pretrained=True)
        last_layer = nn.Sequential(
            *list(vgg_model.classifier.children())[:-1]
            )
        vgg_model.classifier = last_layer
        
        self.encoder = vgg_model
        self.encoder.eval()
        self.transform = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    # transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)) # Standard Normalization
                    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)) #ImageNet Normalization
                    ])