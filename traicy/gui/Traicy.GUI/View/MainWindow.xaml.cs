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
using System.Windows.Input;
using System.Drawing;

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
            if (!Directory.Exists(@"configs"))
            {
                Directory.CreateDirectory(@"configs");
            }
            if (!File.Exists(@"configs\settings.json"))
            {
                _settings = new SettingsController().CreateJsonFileWithStandardValues();
            }

            if (_settings == null)
            {
                _settings = JsonParser.DeserializeFromJson<SettingProperties>(@"configs\settings.json");
            }

            _camera = new WebCam();

        }

        private void OnSettingsChanged(ISettingProperties settings)
        {
            _settings = settings;
        }

        private void BackgroundWorkerOnProgressChanged(object sender, ProgressChangedEventArgs progressChangedEventArgs)
        {
            try
            {
                WebcamVideo.Source = progressChangedEventArgs.UserState as ImageSource;
            }
            catch (Exception e)
            {
                Logger.Log(e.Message);
            }
        }

        private void Worker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            try
            {
                _camera.Disconnect();
                ConnectButton.Content = "Kamera verbinden";

                //TODO: statischen string als Resource hinterlegen 
                WebcamVideo.Source = new BitmapImage(new Uri("pack://application:,,,/Traicy.GUI;component/resources/no-camera.png"));
            }
            catch (Exception exception)
            {
                Logger.Log(exception.Message);
            }
        }

        private void Worker_DoWork(object sender, DoWorkEventArgs e)
        {
            while (!_backgroundWorker.CancellationPending)
            {
                try
                {
                    _camera.Update();

                    WebcamHelper helper = new WebcamHelper();

                
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
                    //log problems using the camera
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

        private void StartObjectDetection()
        {
            if (_camera.IsConnected())
            {
                ButtonStartObjectDetection.Content = "Verarbeitung...";

                var absoluteFilteredImagePath = SaveImage();

                PythonConnector pythonConnector =
                    new PythonConnector { PythonInterpreterPath = _settings.GuiSettings.PythonInterpreterPath };
                string prediction = pythonConnector.GetPrediction(absoluteFilteredImagePath);

                FilteredImagesWindow filteredImagesWindow = null;
                var chunkedImage = WebcamHelper.GetBitmapImageFromSource(@"chunked\chunked.png");
                SetImageSource(chunkedImage);

                if (!prediction.Contains("error") && _settings.GuiSettings.ShowFilteredImagesIsEnabled)
                {
                    filteredImagesWindow = new FilteredImagesWindow();
                    filteredImagesWindow.Show(); //Open window that shows the filtered Images created from the image filter
                }

                if (_settings.GuiSettings.TextToSpeechIsEnabled)
                {
                    TextToSpeech textToSpeech = new TextToSpeech();
                    textToSpeech.InvokeAsyncTextToSpeech(prediction);
                }
                else
                {
                    //TODO: TESTEN!! andere Ausgabe des Ergebnisses (textuell) --> Python (Chunking)
                    //if (filteredImagesWindow != null)
                    //{
                    //    filteredImagesWindow.ResultTextBlock.Text = prediction;
                    //}

                }

                ButtonStartObjectDetection.Content = "Starte Objekterkennung";
            }
        }

        private void ButtonStartObjectDetection_OnClick(object sender, RoutedEventArgs e)
        {
            StartObjectDetection();
        }

        private void KeyDownObjectDetection(object sender, KeyEventArgs e)
        {
            if ((e.Key == Key.P))
            {
                StartObjectDetection();
            }
        }

        private void ButtonBase_OnClick(object sender, RoutedEventArgs e)
        {
            try
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
            catch (Exception exception)
            {
                Logger.Log(exception.Message);
            }
           
        }

        //TODO: löschen?
        private void ButtonTakePicture_OnClick(object sender, RoutedEventArgs e)
        {
            if (_camera.IsConnected())
            {
                SaveImage();
            }
        }

        private string SaveImage()
        {
            WebcamHelper helper = new WebcamHelper();
            var picture = _camera.GetBitmap();
            var absolutePath = helper.TakePicture(picture);
            return absolutePath;
        }

        private void SetImageSource(Bitmap image)
        {
            WebcamHelper helper = new WebcamHelper();
            var webcamFrame = helper.ImageSourceForBitmap(image);
            WebCamPicture.Source = webcamFrame;
        }

        //call to avoid exception when closing the window without disconnecting the camera
        private void Window_Closing(object sender, CancelEventArgs e)
        {
            _backgroundWorker.CancelAsync();
        }
    }
}
