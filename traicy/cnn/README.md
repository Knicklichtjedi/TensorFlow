## CNN folder

**This folder contains the code for the TensorFlow implementation of the object detection with python.**

**Folder**

- MNIST-data: Contains all image and label data of MNIST. Downloaded automaticly when training the number model is started.

- model_letter: All model files that belong to the CNN that predicts letters.

- model_number: All model files that belong to the CNN that predicts digits.

- TRAICY_data: This folder is filled with image data when _prepare_data.py_ is executed. 

**Scripts**

- initialize_dataset.py: Uses the data in TRAICY_data and creates an serialized data set object.

- LETTER_load_model_with_fully_custom_estimator.py: Loads the letter model from its folder.

- LETTER_train_model_with_fully_custom_estimator.py: Starts the training of the letter model.

- NUMBER_load_model_with_fully_custom_estimator.py: Loads the number model from its folder.

- NUMBER_train_model_with_fully_custom_estimator.py: Starts the training of the number model.

- predict_with_ce.py: When started the script needs 2 launch arguments. A path to an image and an identifier for the model to use for prediction ("number" or "letter").