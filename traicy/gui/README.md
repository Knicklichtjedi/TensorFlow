## GUI folder

**This folder contains the code for the implementation of the graphical user interface.**

**Folder**

- Traicy.GUI: contains libraries and all subfolders with data used for the application

    - Commands: contains the base class that is used for all commands in the view

    - Contracts: contains the base classes and interfaces that are implemented

    - Data: folder for all setting classes and data classes that are used for the prediction

    - Logic: contains all classes that are responsible for processing, parsing, logging, handling the settings, the object detection and helping functions

    - Properties: contains the AssemblyInfo, settings and resources of the application

    - View: all *.xaml and *.xaml.cs files that represent the user interface (main window and settings)

    - ViewModels: contains the corresponding view models of the main window and the settings window

    - python_resources: contains all python-files that are needed to execute the object detection (models, modules, filters and neural network files)

    - resources: contains icons used for the user interface

**Scripts**

#### Base classes

- DelegateCommand.cs: base class that is used for all commands in the view

- ViewModelBase.cs: base class for implementing INotifyPropertyChanged interface so that OnPropertyChanged can be used in combination with bindings in the view

#### Settings

- FilterSettings.cs: contains the settings object used for the python filters such as chromakeying

- GuiSettings.cs: represents all interface settings

- ImageSettings.cs: contains the python image settings such as the dimension

- LoadingSettings.cs: contains the image settings (which image files can be read (.png, .jpg, ...))

- SettingProperties.cs: wrapper for all settings that is used for saving the settings to .JSON-file

- SettingsController.cs: sets standard values for the settings if they don't exist and reads and writes the settings from / to the .JSON-file

#### Parser

- JsonParser.cs: class that is responsible for reading and writing the settings from / to the .JSON-file

- PythonOutputParser.cs: parses several types that are used for object detection and processing in the view to needed format

#### Logging

- Logger.cs: logs all errors or exceptions in a log file (log.txt)

#### Object Detection

- Prediction.cs: data class that represents an prediction object containing the value and the percentage

- PythonConnector.cs: invokes the object detection and parses the results

- ObjectDetection.cs: starts process and calls python scripts that execute the object detection and receives the result

#### Output

- TextToSpeech.cs: executes the text-to-speech algorithm

- WebcamHelper.cs: provides methods for converting to a format that can be displayed in the gui

#### View

- MainWindow.xaml: Contains the xaml-code for the main window of the gui

- MainWindow.xaml.cs: code behind of MainWindow.xaml

- MainViewModel.cs: contains the logic of the main view with OnPropteryChanged events and bindings; handles the camera input, loading the images from the disk, output and object detection

- SettingsWindow.xaml: Contains the xaml-code for the settings window of the gui

- SettingsWindow.xaml.cs: code behind of SettingsWindow.xaml

- SettingsViewModel.cs: contains the logic of the settings view with OnPropteryChanged events and bindings; handles changes in the settings 

**For files in python_resources folder check the README.md-files of the python components (cnn, configs, filters)**
