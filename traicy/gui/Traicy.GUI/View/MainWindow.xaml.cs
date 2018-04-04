using System.ComponentModel;
using System.Drawing;
using System.Drawing.Imaging;
using System.Windows;
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

            _camera = new WebCam();
        }

        private void Worker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            _camera.Disconnect();
            ConnectButton.Content = "&Connect";
        }

        private void Worker_DoWork(object sender, DoWorkEventArgs e)
        {
            while (!_backgroundWorker.CancellationPending)
            {
                _camera.Update();

                WebcamHelper helper = new WebcamHelper();
                WebcamVideo.Source = helper.ImageSourceForBitmap(_camera.CalcBitmap());
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

        private void TakePicture()
        {
            Bitmap image = _camera.GetBitmap();
            string filename = "test.png";
            image.Save(@"/images/" + filename, ImageFormat.Png);
            //TODO: Image an Python übergeben oder so lassen, dass Python die Bilder über Ordnerstruktur einliest?
        }

        private void ButtonStartObjectDetection_OnClick(object sender, RoutedEventArgs e)
        {
            //TakePicture();
            IronPythonConnection ironPythonConnection = new IronPythonConnection();
            ironPythonConnection.InitializeIronPython();
            string prediction = ironPythonConnection.GetPrediction();
            TextToSpeech textToSpeech = new TextToSpeech();
            textToSpeech.InvokeAsyncTextToSpeech(prediction);

        }
        
        private void ButtonBase_OnClick(object sender, RoutedEventArgs e)
        {
            if (!_camera.IsConnected())
            {
                _camera.Connect();
                ConnectButton.Content = "&Disconnect";
                _backgroundWorker.RunWorkerAsync();
            }
            else
            {
                _backgroundWorker.CancelAsync();
            }

            _camera.Connect();
        }
    }
}
