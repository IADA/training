from __future__ import unicode_literals

from threading import Lock
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.preprocessing import image
import numpy as np

# Singleton http://www.denzow.me/entry/2018/01/28/171416
class NN_Model:
    _unique_instance = None
    _lock = Lock()
    _model = None

    def __new__(cls):
        raise NotImplementedError('Cannot initialize via Constructor')

    @classmethod
    def __internal_new__(cls):
        return super().__new__(cls)

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if not cls._unique_instance:
                cls._unique_instance = cls.__internal_new__()
        return cls._unique_instance

    def setup(cls):
        with cls._lock:
            if not cls._model:
                cls._model = VGG16(weights='imagenet')

    def predict(cls, file_path):
        with cls._lock:
            img = image.load_img(file_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            preds = cls._model.predict(preprocess_input(x))
            results = decode_predictions(preds, top=5)[0]
        return results
