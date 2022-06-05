import os
from datetime import datetime

from tensorflow.keras.layers import Conv2D, Flatten, Dense, MaxPool2D, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.applications.efficientnet import EfficientNetB0
import tensorflow as tf
from sklearn import metrics
from keras.preprocessing.image import ImageDataGenerator, load_img
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
import numpy as np

from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg19 import VGG19


def efficientNet_B0(retrain, train_generator):
    """
    Creates and returns the efficientNet_b0 model
    params:
    retrain: specifies whether transferlearnign based on the imagedataset is performed or not.
    train_generator: the generator object containing the imagedata

    return: compiled model
    """
    if not retrain:
        weights = None
    else:
        weights = "imagenet"

    base_model = EfficientNetB0(include_top=False, weights=weights)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    predictions = Dense(train_generator.num_classes, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    if (retrain):
        for layer in base_model.layers:
            layer.trainable = False
    model.summary()
    model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def efficientNet_B7(retrain, train_generator):
    """
       Creates and returns the efficientNet_b7 model
       params:
       retrain: specifies whether transferlearnign based on the imagedataset is performed or not.
       train_generator: the generator object containing the imagedata

       return: compiled model
       """
    if not retrain:
        weights = None
    else:
        weights = "imagenet"
    base_model = EfficientNetB0(include_top=False, weights=weights)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    predictions = Dense(train_generator.num_classes, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    if retrain:
        for layer in base_model.layers:
            layer.trainable = False
    model.summary()
    model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def resnet50(retrain, train_generator):
    """
       Creates and returns the resnet50 model
       params:
       retrain: specifies whether transferlearnign based on the imagedataset is performed or not.
       train_generator: the generator object containing the imagedata

       return: compiled model
       """
    if not retrain:
        weights = None
    else:
        weights = "imagenet"
    base_model = ResNet50(include_top=False, weights=weights)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    predictions = Dense(train_generator.num_classes, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    if retrain:
        for layer in base_model.layers:
            layer.trainable = False
    model.summary()
    model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def VGG_16(retrain, train_generator):
    """
       Creates and returns the VGG16 model
       params:
       retrain: specifies whether transferlearnign based on the imagedataset is performed or not.
       train_generator: the generator object containing the imagedata

       return: compiled model
       """
    if not retrain:
        weights = None
    else:
        weights = "imagenet"
    base_model = VGG16(include_top=False, weights=weights)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    predictions = Dense(train_generator.num_classes, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    if retrain:
        for layer in base_model.layers:
            layer.trainable = False
    model.summary()
    model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def VGG_19(retrain, train_generator):
    """
       Creates and returns the VGG19 model
       params:
       retrain: specifies whether transferlearnign based on the imagedataset is performed or not.
       train_generator: the generator object containing the imagedata

       return: compiled model
       """
    if not retrain:
        weights = None
    else:
        weights = "imagenet"
    base_model = VGG19(include_top=False, weights=weights)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    predictions = Dense(train_generator.num_classes, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    if retrain:
        for layer in base_model.layers:
            layer.trainable = False
    model.summary()
    model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=['accuracy'])
    return model


if __name__ == "__main__":
    print("")
