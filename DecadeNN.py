from keras.models import Sequential
from keras import Input
from keras import backend as K
from keras import utils
import numpy as np
from PIL import Image
import os
import shutil
import splitfolders
import matplotlib.pyplot as plt
from keras import layers

# Delete Old Data
if os.path.exists('Data/YearOutput') and os.path.isdir('Data/YearOutput'):
    shutil.rmtree('Data/YearOutput')

# Create Training, Testing, Validation Folders
splitfolders.ratio('Data/Year', output='Data/YearOutput', seed=1337, ratio=(.8, .1, .1))

# Settings
img_width, img_height = 268, 182
train_data_dir = 'Data/YearOutput/train'
test_data_dir = 'Data/YearOutput/test'
validation_data_dir = 'Data/YearOutput/val'
classCount = len(next(os.walk('Data/Year'))[1])
print("Class Count: " + str(classCount))
epochs = 25
batch_size = 16

# Change Shape Based On ARGB vs RGBA
if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

# Create Training Data
x_train = []
y_train = []
classIterator = -1
trainDirectory = os.fsencode(train_data_dir)
for subdir, dirs, files in os.walk(trainDirectory):
    for sub in dirs:
        classIterator+=1
        print('Found train class number:' + str(classIterator) + ' named: ' + str(os.fsdecode(sub)))
        sub = os.path.join(trainDirectory, sub)
        for file in os.listdir(sub):
            file = os.path.join(sub, file)
            image = Image.open(file).convert('RGB')
            img = np.array(image)
            x_train.append(img)
            y_train.append(classIterator)

x_train = np.array(x_train)
x_train = x_train.astype("float32") / 255
y_train = np.array(y_train)
y_train = utils.to_categorical(y_train, classCount)

# Create Testing Data
x_test = []
y_test = []
classIterator = -1
testDirectory = os.fsencode(test_data_dir)
for subdir, dirs, files in os.walk(testDirectory):
    for sub in dirs:
        classIterator+=1
        print('Found test class number:' + str(classIterator) + ' named: ' + str(os.fsdecode(sub)))
        sub = os.path.join(testDirectory, sub)
        for file in os.listdir(sub):
            file = os.path.join(sub, file)
            image = Image.open(file).convert('RGB')
            img = np.array(image)
            x_test.append(img)
            y_test.append(classIterator)

x_test = np.array(x_test)
x_test = x_test.astype("float32") / 255
y_test = np.array(y_test)
y_test = utils.to_categorical(y_test, classCount)

# Create Model
model = Sequential(
    [
        Input(shape=input_shape),

        layers.Convolution2D(128, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),

        layers.Convolution2D(128, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),

        layers.Convolution2D(128, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),

        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.5),
        layers.Dense(classCount, activation="softmax"),
    ]
)

# Compile Model
model.compile(loss="categorical_crossentropy",
              optimizer="adam",
              metrics=["accuracy"])

# Fit Model
history = model.fit(
    x_train,
    y_train,
    batch_size= batch_size,
    epochs=epochs,
    validation_split=0.1)

# Evaluate And Save Model
score = model.evaluate(x_test, y_test)
print("Test loss:", score[0])
print("Test accuracy:", score[1])
model.save("Years.h5")
print("Saved model to disk")

# Create Data For Graph
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs_range = range(epochs)

# Create Graph
plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')
plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()