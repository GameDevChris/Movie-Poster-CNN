import numpy as np
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import os
from keras.models import load_model

def Genre(url):

    # Get Image And Format
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    img = np.array(image.resize((268, 182)))
    img = img.reshape(1, 268, 182, 3)
    img = img / 255.0

    # Use Model
    model = load_model('Genres.h5')
    out = model.predict(img)

    # Sort Classes
    classes = [item for item in os.listdir('Data/Genre') if os.path.isdir(os.path.join('Data/Genre', item))]
    results = []
    text = ''
    for i in range(len(classes)):
        print(str(i))
        print(str(classes[i]))
        results.append(out[0][i])
        text += classes[i] + ": " + str(float("{:.2f}".format(out[0][i]))*100) + '% / '
    indices = np.argpartition(np.array(results), -5)[-5:]
    resultsOut = [results[i] for i in indices]
    classOut = [classes[i] for i in indices]
    class_pos = [i for i, _ in enumerate(classOut)]

    # Create Plot And Output
    fig = plt.figure()
    plt.style.use('ggplot')
    plt.bar(class_pos, resultsOut, color='green')
    plt.ylabel("% Membership")
    plt.title("Genre Prediction")
    plt.xticks(class_pos, classOut)
    output = (text, plt)
    return output

def Decade(url):

    # Get Image And Format
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    img = np.array(image.resize((268, 182)))
    img = img.reshape(1, 268, 182, 3)
    img = img / 255.0

    # Use Model
    model = load_model('Years.h5')
    out = model.predict(img)

    # Sort Classes
    classes = [item for item in os.listdir('Data/Year') if os.path.isdir(os.path.join('Data/Year', item))]
    results = []
    text = ''
    for i in range(len(classes)):
        print(str(i))
        print(str(classes[i]))
        results.append(out[0][i])
        text += classes[i] + ": " + str(float("{:.2f}".format(out[0][i]))*100) + '% / '

    indices = np.argpartition(np.array(results), -5)[-5:]

    resultsOut = [results[i] for i in indices]
    classOut = [classes[i] for i in indices]

    class_pos = [i for i, _ in enumerate(classOut)]

    # Create Plot And Output
    fig = plt.figure()
    plt.style.use('ggplot')
    plt.bar(class_pos, resultsOut, color='green')
    plt.ylabel("% Membership")
    plt.title("Decade Prediction")
    plt.xticks(class_pos, classOut)
    output = (text, plt)
    return output

