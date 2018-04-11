using System;
using System.ComponentModel;
using System.Drawing;
using System.Drawing.Imaging;
using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using MetriCam;
using Traicy.GUI.Logic;

namespace Traicy.GUI.View
{
    /// <summary>
    /// Interaktionslogik für MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private readonly WebCam _camera;
        private readonly BackgroundWorker _backgroundWorker = new BackgroundWorker();

        public MainWindow()
        {
            InitializeComponent();

            _backgroundWorker.DoWork += Worker_DoWork;
            _backgroundWorker.RunWorkerCompleted += Worker_RunWorkerCompleted;

            _backgroundWorker.WorkerSupportsCancellation = true;
            _backgroundWorker.WorkerReportsProgress = true;

            _backgroundWorker.ProgressChanged += BackgroundWorkerOnProgressChanged;

            _camera = new WebCam();
        }

        private void BackgroundWorkerOnProgressChanged(object sender, ProgressChangedEventArgs progressChangedEventArgs)
        {
            WebcamVideo.Source = progressChangedEventArgs.UserState as ImageSource;
        }

        private void Worker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            _camera.Disconnect();
            ConnectButton.Content = "Kamera verbinden";

            WebcamVideo.Source = new BitmapImage(
                new Uri("pack://application:,,,/Traicy.GUI;component/resources/no-camera.png"));
        }

        private void Worker_DoWork(object sender, DoWorkEventArgs e)
        {
            while (!_backgroundWorker.CancellationPending)
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
            ButtonStartObjectDetection.Content = "Verarbeitung...";

            //TODO: TakePicture?
            
            PythonConnector pythonConnector = new PythonConnector();
            //pythonConnector.ExecutePythonScript();
            //pythonConnector.ExecutePythonScript2();
            string prediction = pythonConnector.GetPrediction();
            TextToSpeech textToSpeech = new TextToSpeech();
            textToSpeech.InvokeAsyncTextToSpeech(prediction);

            ButtonStartObjectDetection.Content = "Starte Objekterkennung";

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

        private void ButtonTakePicture_OnClick(object sender, RoutedEventArgs e)
        {
            if (_camera.IsConnected())
            {
                WebcamHelper helper = new WebcamHelper();
                var picture = _camera.GetBitmap();
                var webcamFrame = helper.ImageSourceForBitmap(picture);
                WebCamPicture.Source = webcamFrame;
                helper.TakePicture(picture);
            }
        }

        //call to avoid exception when closing the window without disconnecting the camera
        private void Window_Closing(object sender, CancelEventArgs e)
        {
            _backgroundWorker.CancelAsync();
        }
    }
}
