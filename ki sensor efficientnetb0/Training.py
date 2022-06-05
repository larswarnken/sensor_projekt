import os
from datetime import datetime

import tensorflow as tf


def train_model(model, train_generator, valid_generator, epochs):
    """
    Fits the model to the given training data for the specified number of epochs
    params:
            model: model to be trained
            train_generator: generator object containing the trainingdata
            valid_generator: generator object containing the validationdata
            epochs: number of epochs to be trained

    returns: trained model
    """
    #directory for the tensorboard data
    log_dir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S") + "_Efficientnet"
    tf_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
    model.fit(train_generator, validation_data=valid_generator, epochs=epochs, callbacks=[tf_callback])
    model.save('myData/models/'+datetime.now().strftime("%Y%m%d-%H%M%S"))
    return model
