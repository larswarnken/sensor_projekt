import Read_Data
import Model
import Training
import Evaluation
import File_handling


def run():
    """
    Methode, zur ge
    """
    dir_path = "myData/imageData/dataset sensor"
    train, validation, test = Read_Data.createDataGenerators(dir_path, 450, 300, 5)
    model = Model.efficientNet_B0(True, train)
    File_handling.write_model_summary_to_file(model)
    model = Training.train_model(model, train, validation, 15)
    z, accuracy = Evaluation.evaluate_model(model, test)
    print(f'accuracy: {accuracy}')
    print(f'loss: {z}')


if __name__ == "__main__":
    run()
