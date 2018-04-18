using System;
using System.ComponentModel;
using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using MetriCam;
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
        private bool _textToSpeechIsEnabled;

        public MainWindow()
        {
            InitializeComponent();

            _textToSpeechIsEnabled = true;

            //custom setting events
            EventHandling.TextToSpeechEvent += OnTextToSpeechChanged;

            _backgroundWorker.DoWork += Worker_DoWork;
            _backgroundWorker.RunWorkerCompleted += Worker_RunWorkerCompleted;

            _backgroundWorker.WorkerSupportsCancellation = true;
            _backgroundWorker.WorkerReportsProgress = true;

            _backgroundWorker.ProgressChanged += BackgroundWorkerOnProgressChanged;

            _camera = new WebCam();

            JsonTest();
        }

        private void JsonTest()
        {
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

            IGuiSettings guiSettings = new GuiSettings() { TextToSpeechIsEnabled = true };

            ImageSettings imageSettings = new ImageSettings() { Border = 0, Dimension = 0, DimensionSmall = 0 };

            ISettingProperties settingsProperties = new SettingProperties
            {
                FilterSettings = filter,
                ImageSettings = imageSettings
            };

            JsonParser.SerializeToJson(settingsProperties, @"settingsTest.json");
        }

        private void OnTextToSpeechChanged(bool isEnabled)
        {
            _textToSpeechIsEnabled = isEnabled;
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
            WebcamVideo.Source = new BitmapImage(
                new Uri("pack://application:,,,/Traicy.GUI;component/resources/no-camera.png"));
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
            new SettingsWindow().ShowDialog();
        }

        private void ButtonStartObjectDetection_OnClick(object sender, RoutedEventArgs e)
        {

            if (_camera.IsConnected())
            {
                ButtonStartObjectDetection.Content = "Verarbeitung...";

                var absolutePath = SetImageSource();
                PythonConnector pythonConnector = new PythonConnector();
                string prediction = pythonConnector.GetPrediction(absolutePath);

                if (_textToSpeechIsEnabled)
                {
                    TextToSpeech textToSpeech = new TextToSpeech();
                    textToSpeech.InvokeAsyncTextToSpeech(prediction);
                }
                else
                {
                    //TODO: andere Ausgabe des Ergebnisses (textuell)
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
