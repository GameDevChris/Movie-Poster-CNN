import os

from PIL import Image
import numpy as np
from keras import utils
from keras.models import load_model

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
genre_test_data_dir = 'Data/TestingData/GenreTest'
decade_test_data_dir = 'Data/TestingData/YearTest'

def GenreTest():
    print("-----")
    print("Testing the Genre CNN Model:")
    x_test = []
    y_test = []
    classIterator = -1
    testDirectory = os.fsencode(genre_test_data_dir)
    for subdir, dirs, files in os.walk(testDirectory):
        for sub in dirs:
            classIterator += 1
            sub = os.path.join(testDirectory, sub)
            for file in os.listdir(sub):
                file = os.path.join(sub, file)
                image = Image.open(file).convert('RGB')
                img = np.array(image)
                x_test.append(img)
                y_test.append(classIterator)
    x_test = np.array(x_test).astype("float32") / 255
    y_test = utils.to_categorical(np.array(y_test), len(next(os.walk(genre_test_data_dir))[1]))
    model = load_model('Genres.h5')
    score = model.evaluate(x_test, y_test)
    print("Genre Test loss:", score[0])
    print("Genre Test accuracy:", score[1])
    print("-----")

def DecadesTest():
    print("-----")
    print("Testing the Decade CNN Model:")
    x_test = []
    y_test = []
    classIterator = -1
    testDirectory = os.fsencode(decade_test_data_dir)
    for subdir, dirs, files in os.walk(testDirectory):
        for sub in dirs:
            classIterator += 1
            sub = os.path.join(testDirectory, sub)
            for file in os.listdir(sub):
                file = os.path.join(sub, file)
                image = Image.open(file).convert('RGB')
                img = np.array(image)
                x_test.append(img)
                y_test.append(classIterator)
    x_test = np.array(x_test).astype("float32") / 255
    y_test = utils.to_categorical(np.array(y_test), len(next(os.walk(decade_test_data_dir))[1]))
    model = load_model('Years.h5')
    score = model.evaluate(x_test, y_test)
    print("Decade Test loss:", score[0])
    print("Decade Test accuracy:", score[1])
    print("-----")

GenreTest()
DecadesTest()
