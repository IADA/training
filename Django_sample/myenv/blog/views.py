# coding: utf-8
from django.shortcuts import render
from django.utils import timezone
from .models import Post

from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.preprocessing import image
import numpy as np
import sys

# Create your views here.
def post_list(request):
    model = VGG16(weights='imagenet')
    img = image.load_img("banana.jpg", target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    preds = model.predict(preprocess_input(x))
    results = decode_predictions(preds, top=5)[0]

    return render(request, 'blog/post_list.html', {'results':results})
