from sklearn import svm
from sklearn.externals import joblib
from PIL import Image
import os
import numpy


class Recognizer:
    def __init__(self):
        self.data = []
        self.values = []
        self.svc = svm.SVC(gamma=0.001, kernel='linear', C=100)
        self.downscale_size = (32, 32)

    def _load(self, path, value):
        images = os.listdir(path)
        for filename in images:
            img = Image.open(path+'/'+filename)
            img = img.resize(self.downscale_size, Image.BILINEAR)
            self.data.append(numpy.array(img.getdata()).flatten())
            self.values.append(value)

    def load(self):
        self._load('training-images/0', 0)
        self._load('training-images/1', 1)
        self._load('training-images/2', 2)
        self._load('training-images/3', 3)
        self._load('training-images/4', 4)
        self._load('training-images/5', 5)
        self._load('training-images/6', 6)
        self._load('training-images/7', 7)
        self._load('training-images/8', 8)
        self._load('training-images/9', 9)

    def train(self):
        if os.path.isfile('trained.dat'):
            self.svc = joblib.load('trained.dat')
        else:
            self.load()
            np_data = self.data
            np_values = self.values
            self.svc.fit(np_data, np_values)
            joblib.dump(self.svc, 'trained.dat', compress=9)

    def predict(self, image):
        image = image.resize(self.downscale_size, Image.BILINEAR)
        input_image = numpy.array(image.getdata()).flatten().reshape(1, -1)
        return int(self.svc.predict(input_image))
