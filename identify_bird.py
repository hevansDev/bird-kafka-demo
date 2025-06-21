from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch

# Try AutoImageProcessor instead of AutoFeatureExtractor
try:
    processor = AutoImageProcessor.from_pretrained("chriamue/bird-species-classifier")
    model = AutoModelForImageClassification.from_pretrained("chriamue/bird-species-classifier")
    
    # Load and preprocess your image
    image = Image.open("robin.jpeg")
    inputs = processor(images=image, return_tensors="pt")
    
    # Make prediction
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    # Get the predicted class
    predicted_class_idx = predictions.argmax().item()
    confidence = predictions.max().item()
    
    print(f"Predicted class index: {predicted_class_idx}")
    print(f"Confidence: {confidence:.2%}")
    
except Exception as e:
    print(f"Error with AutoImageProcessor: {e}")