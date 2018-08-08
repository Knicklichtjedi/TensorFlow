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
using System.Threading;
using Microsoft.Win32;

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
		private bool _isImageFromDisk;
		private string _imageFromDisk;

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
				ConnectButton.Content = Properties.Resources.ConnectWebcam;

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
			//if the webcam has been connected or the user has choosen an image from disk
			if (_camera.IsConnected() || WebcamVideo.Source != null)
			{
				Dispatcher.BeginInvoke(new Action(() =>
				{
					ButtonStartObjectDetection.Content = Properties.Resources.Processing;
					
				}));

				string imagePath;

				if (_isImageFromDisk)
				{
					//TODO: 
					imagePath = _imageFromDisk;
					Thread.Sleep(5000);
				}
				else
				{
					var absoluteFilteredImagePath = SaveImage();
					imagePath = absoluteFilteredImagePath;

				}

				PredictImageFromPath(imagePath);

				Dispatcher.BeginInvoke(new Action(() =>
				{
					ButtonStartObjectDetection.Content = Properties.Resources.StartObjectDetection;
				}));
			}
		}

		private void PredictImageFromPath(string absoluteFilteredImagePath)
		{
			PythonConnector pythonConnector =
				new PythonConnector {PythonInterpreterPath = _settings.GuiSettings.PythonInterpreterPath};
			string prediction = pythonConnector.GetPrediction(absoluteFilteredImagePath);



			if (!prediction.Contains("Fehler"))
			{
				var chunkedImage = WebcamHelper.GetBitmapImageFromSource(@"chunked\chunked.png");
				SetImageSource(chunkedImage);
				if(_settings.GuiSettings.ShowFilteredImagesIsEnabled)
				{

					var filteredImagesWindow = new FilteredImagesWindow();
					filteredImagesWindow.Show(); //Open window that shows the filtered Images created from the image filter
				}
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

		private void ButtonConnectWebcam_OnClick(object sender, RoutedEventArgs e)
		{
			try
			{
				if (!_camera.IsConnected())
				{
					_camera.Connect();
					ConnectButton.Content = "Verbindung trennen";
					_isImageFromDisk = false;

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

		/// <summary>
		/// User chooses image from disk which is used for object detection.
		/// If the button for choosing the image is clicked, an open file dialog opens from which the user can choose the image which is used for object detection. 
		/// The image is displayed on the left side of the gui (live webcam video). The result is displayed on the right side of the gui.
		/// </summary>
		/// <param name="sender">object that triggered the event</param>
		/// <param name="e">optional event arguments for further processing</param>
		private void ButtonTakePicture_OnClick(object sender, RoutedEventArgs e)
		{
			//if (_camera.IsConnected())
			//{
				//SaveImage();

			try
			{
				OpenFileDialog openFileDialog =
					new OpenFileDialog { Filter = "PNG (*.png)|*.png|JPEG (*.jpg;*.jpeg)|*.jpg;*.jpeg|All files (*.*)|*.*" };

				if (openFileDialog.ShowDialog() == true)
				{
					//_pythonInterpreterPath = openFileDialog.FileName;
					string fileName = openFileDialog.FileName;
					WebcamVideo.Source = new BitmapImage(new Uri(fileName));
					_imageFromDisk = fileName;
				}

				_isImageFromDisk = true;

			}
			catch (FileFormatException fileFormatException)
			{
				Logger.Log(fileFormatException.Message);
			}
				
			//}
		}

		//TODO: auslagern
		private string SaveImage()
		{
			WebcamHelper helper = new WebcamHelper();
			var picture = _camera.GetBitmap();
			var absolutePath = helper.TakePicture(picture);
			return absolutePath;
		}


		//TODO: auslagern
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
