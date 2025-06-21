from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch

# Load the model and processor
processor = AutoImageProcessor.from_pretrained("chriamue/bird-species-classifier")
model = AutoModelForImageClassification.from_pretrained("chriamue/bird-species-classifier")

# Load and preprocess your image
image = Image.open("pigeon1.jpg")
inputs = processor(images=image, return_tensors="pt")

# Make prediction
with torch.no_grad():
    outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

# Get the predicted class
predicted_class_idx = predictions.argmax().item()
confidence = predictions.max().item()

# Convert class index to species name
if hasattr(model.config, 'id2label'):
    species_name = model.config.id2label[predicted_class_idx]
    print(f"Predicted species: {species_name}")
    print(f"Confidence: {confidence:.2%}")
else:
    print(f"Predicted class index: {predicted_class_idx}")
    print(f"Confidence: {confidence:.2%}")
    print("Label mapping not found in model config")

# Get top 5 predictions with species names
top5_prob, top5_idx = torch.topk(predictions, 5)
print(f"\nTop 5 predictions:")

for i in range(5):
    class_idx = top5_idx[0][i].item()
    prob = top5_prob[0][i].item()
    
    if hasattr(model.config, 'id2label'):
        species_name = model.config.id2label[class_idx]
        print(f"{i+1}. {species_name}: {prob:.2%}")
    else:
        print(f"{i+1}. Class {class_idx}: {prob:.2%}")