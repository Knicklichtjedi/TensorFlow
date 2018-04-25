using System;
using System.ComponentModel;
using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using MetriCam;
using System.IO;
using Traicy.GUI.Logic;
using Traicy.GUI.Contracts;
using Traicy.GUI.Data;

namespace Traicy.GUI.View
{
    /// <summary>
    /// Interaktionslogik für MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private readonly WebCam _camera;
        private readonly BackgroundWorker _backgroundWorker = new BackgroundWorker();
        private ISettingProperties _settings; 

        public MainWindow()
        {
            InitializeComponent();

            //custom setting events
            //EventHandling.TextToSpeechEvent += OnTextToSpeechChanged;
            EventHandling.SettingsChangedEvent += OnSettingsChanged;

            _backgroundWorker.DoWork += Worker_DoWork;
            _backgroundWorker.RunWorkerCompleted += Worker_RunWorkerCompleted;

            _backgroundWorker.WorkerSupportsCancellation = true;
            _backgroundWorker.WorkerReportsProgress = true;

            _backgroundWorker.ProgressChanged += BackgroundWorkerOnProgressChanged;

            //load settings only at the start of the application
            if (!File.Exists(@"configs\settings.json"))
            {
                CreateJsonFile();
            }
            _settings = JsonParser.DeserializeFromJson<SettingProperties>(@"configs\settings.json"); 
            //_settings = JsonParser.DeserializeFromJson<SettingProperties>("settingsTest.json"); 

            _camera = new WebCam();

        }

        private void OnSettingsChanged(ISettingProperties settings)
        {
            _settings = settings;
        }

        private void CreateJsonFile()
        {

            //TODO: Werte auf Standard einstellen
            FilterSettings filter = new FilterSettings()
            {
                Canny = 0,
                BinaryGauss = 0,
                BinaryThreshold = 0,
                GreenBrightness = 0,
                GreenHigh = 0,
                GreenLow = 0,
                GreenSaturation = 0
            };

            GuiSettings guiSettings = new GuiSettings { TextToSpeechIsEnabled = true, ShowFilteredImagesIsEnabled = true, PythonInterpreterPath = @"C:\Users\Eva\Anaconda3\envs\customTFLearn\python.exe" };

            ImageSettings imageSettings = new ImageSettings { Border = 0, Dimension = 0, DimensionSmall = 0 };

            ISettingProperties settingsProperties = new SettingProperties
            {
                FilterSettings = filter,
                ImageSettings = imageSettings,
                GuiSettings = guiSettings
            };

            JsonParser.SerializeToJson(settingsProperties, @"configs\settings.json");
        }

        private void BackgroundWorkerOnProgressChanged(object sender, ProgressChangedEventArgs progressChangedEventArgs)
        {
            WebcamVideo.Source = progressChangedEventArgs.UserState as ImageSource;
        }

        private void Worker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            _camera.Disconnect();
            ConnectButton.Content = "Kamera verbinden";

            //TODO: statischen string als Resource hinterlegen 
            WebcamVideo.Source = new BitmapImage(new Uri("pack://application:,,,/Traicy.GUI;component/resources/no-camera.png"));
        }

        private void Worker_DoWork(object sender, DoWorkEventArgs e)
        {
            while (!_backgroundWorker.CancellationPending)
            {
                _camera.Update();

                WebcamHelper helper = new WebcamHelper();

                try
                {
                    //convert camera image (bitmap) to imagesource that is freezable (fixed image) 
                    Freezable webcamFrame = helper.ImageSourceForBitmap(_camera.CalcBitmap()).GetAsFrozen();

                    void UpdateWebCamVideoImageSource()
                    {
                        try
                        {
                            _backgroundWorker.ReportProgress(0, webcamFrame);
                        }
                        catch (Exception exception)
                        {
                            Logger.Log(exception.Message);
                        }
                    }

                    //use Dispatcher to update the objects in the UI from non-UI thread (backgroundWorker)
                    WebcamVideo.Dispatcher.Invoke(UpdateWebCamVideoImageSource);
                }
                catch (Exception exception)
                {
                    Logger.Log(exception.Message);
                }
            }
        }

        private void ButtonSettings_OnClick(object sender, RoutedEventArgs e)
        {
            ShowSettingsWindow();
        }

        private void ShowSettingsWindow()
        {
            new SettingsWindow(_settings).Show();
        }

        private void ButtonStartObjectDetection_OnClick(object sender, RoutedEventArgs e)
        {

            if (_camera.IsConnected())
            {
                ButtonStartObjectDetection.Content = "Verarbeitung...";

                var absoluteFilteredImagePath = SetImageSource();
                PythonConnector pythonConnector =
                    new PythonConnector {PythonInterpreterPath = _settings.GuiSettings.PythonInterpreterPath};
                string prediction = pythonConnector.GetPrediction(absoluteFilteredImagePath);

                if (_settings.GuiSettings.ShowFilteredImagesIsEnabled)
                {
                    new FilteredImagesWindow().Show(); //Open window that shows the filtered Images created from the image filter
                }

                if (_settings.GuiSettings.TextToSpeechIsEnabled)
                {
                    TextToSpeech textToSpeech = new TextToSpeech();
                    textToSpeech.InvokeAsyncTextToSpeech(prediction);
                }
                else
                {
                    //TODO: andere Ausgabe des Ergebnisses (textuell) --> Python (Chunking)
                }

                ButtonStartObjectDetection.Content = "Starte Objekterkennung";
            }

        }

        private void ButtonBase_OnClick(object sender, RoutedEventArgs e)
        {
            if (!_camera.IsConnected())
            {
                _camera.Connect();
                ConnectButton.Content = "Verbindung trennen";

                _backgroundWorker.RunWorkerAsync();
            }
            else
            {
                _backgroundWorker.CancelAsync();
            }
        }

        //TODO: löschen?
        private void ButtonTakePicture_OnClick(object sender, RoutedEventArgs e)
        {
            if (_camera.IsConnected())
            {
                SetImageSource();
            }
        }

        private string SetImageSource()
        {
            WebcamHelper helper = new WebcamHelper();
            var picture = _camera.GetBitmap();
            var webcamFrame = helper.ImageSourceForBitmap(picture);
            WebCamPicture.Source = webcamFrame;
            var absolutePath = helper.TakePicture(picture);
            return absolutePath;
        }

        //call to avoid exception when closing the window without disconnecting the camera
        private void Window_Closing(object sender, CancelEventArgs e)
        {
            _backgroundWorker.CancelAsync();
        }
    }
}
