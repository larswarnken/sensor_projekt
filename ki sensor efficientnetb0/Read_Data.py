import os
from datetime import datetime

from tensorflow.keras.layers import Conv2D, Flatten, Dense, MaxPool2D, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

from keras.preprocessing.image import ImageDataGenerator, load_img


def createDataGenerators(dir, img_height: int, img_width: int, batch_size: int):
    """
    creates the datagenerators

    params:
        dir: path to the dataset
        img_height:
        img_widt:
        batch_size

    returns:
        train_generator: generator for the trainingdata
        valid_generator: generator for the validationdata
        test_generator: generator for the testdata
    """
    train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input,
                                       shear_range=0.1,
                                       zoom_range=0,
                                       horizontal_flip=False,
                                       validation_split=0.4
                                       )

    train_generator = train_datagen.flow_from_directory(
        dir + "/train",
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )

    valid_generator = train_datagen.flow_from_directory(
        dir + "/val",
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )

    test_generator = train_datagen.flow_from_directory(
        dir + "/test",
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )
    return train_generator, valid_generator, test_generator
