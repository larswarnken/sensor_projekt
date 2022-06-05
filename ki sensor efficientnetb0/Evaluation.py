import tensorflow as tf


def evaluate_model(model, test_generator):
    """
    evaluated the model using the testdata

    params:
            model: model to be evaluated
            test_generator: generator containing the testdata

    returns:
            loss: testloss
            accuracy: model accuracy on the testdata
    """
    loss, accuracy = model.evaluate(test_generator)
    return loss, accuracy


if __name__ == "__main__":
    print("")
