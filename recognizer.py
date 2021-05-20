import cv2 as cv
import numpy as np
import tensorflow as tf

class Recognizer():

    def __init__(self):
        self.mnist = tf.keras.datasets.mnist
        (self.x_train, self.y_train), (self.x_test, self.y_test) = self.mnist.load_data()

        self.x_train = tf.keras.utils.normalize(self.x_train, axis=1)
        self.x_test = tf.keras.utils.normalize(self.x_test, axis=1)

        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
        self.model.add(tf.keras.layers.Dense(units=128, activation=tf.nn.relu))
        self.model.add(tf.keras.layers.Dense(units=128, activation=tf.nn.relu))
        self.model.add(tf.keras.layers.Dense(units=10, activation=tf.nn.softmax))

        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        self.model.fit(self.x_train, self.y_train, epochs=4)


        loss, accuracy = self.model.evaluate(self.x_test, self.y_test)
        
        print(f"Accuracy: {accuracy}")
        print(f"Loss: {loss}")

    def Guess(self):

        img = cv.imread(f'./image.png')[:,:,0]
        img = np.invert(np.array([img]))
        prediction = self.model.predict(img)
        return np.argmax(prediction)