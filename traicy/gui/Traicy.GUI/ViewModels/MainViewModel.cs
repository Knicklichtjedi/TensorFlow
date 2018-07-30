using System;
using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using MetriCam;
using Microsoft.Win32;
using Traicy.GUI.Commands;
using Traicy.GUI.Contracts;
using Traicy.GUI.Logic;
using Traicy.GUI.View;

namespace Traicy.GUI.ViewModels
{
	class MainViewModel : ViewModelBase
	{
		private readonly WebCam _camera;
		private readonly BackgroundWorker _backgroundWorker = new BackgroundWorker();
		private bool _isImageFromDisk;
		private string _imageFromDisk;

		public MainViewModel()
		{
			//register background worker events for webcam
			_backgroundWorker.DoWork += Worker_DoWork;
			_backgroundWorker.RunWorkerCompleted += Worker_RunWorkerCompleted;
			_backgroundWorker.ProgressChanged += BackgroundWorkerOnProgressChanged;

			_backgroundWorker.WorkerSupportsCancellation = true;
			_backgroundWorker.WorkerReportsProgress = true;

			_camera = new WebCam();

			ConnectButtonText = Properties.Resources.ConnectWebcam;
			StartObjectDetectionButtonText = Properties.Resources.StartObjectDetection;
		}

		/*-------------------------Properties--------------------------*/
		private ImageSource _liveImage;
		public ImageSource LiveImage
		{
			get => _liveImage;
			set
			{
				_liveImage = value;
				OnPropertyChanged(nameof(LiveImage));
			}
		}

		private ImageSource _liveVideo;
		public ImageSource LiveVideo
		{
			get => _liveVideo;
			set
			{
				_liveVideo = value;
				OnPropertyChanged(nameof(LiveVideo));
			}
		}

		private string _connectButtonText;
		public string ConnectButtonText
		{
			get => _connectButtonText;
			set
			{
				if (_connectButtonText == value)
					return;
				_connectButtonText = value;
				OnPropertyChanged(nameof(ConnectButtonText));
			}
		}

		private string _startObjectDetectionButtonText;
		public string StartObjectDetectionButtonText
		{
			get => _startObjectDetectionButtonText;
			set
			{
				if (_startObjectDetectionButtonText == value)
					return;
				_startObjectDetectionButtonText = value;
				OnPropertyChanged(nameof(StartObjectDetectionButtonText));
			}
		}

		/*-------------------------commands--------------------------*/
		private ICommand _keyDownObjectDetectionCommand;
		private ICommand _buttonConnectWebcamClickCommand;
		private ICommand _buttonStartObjectDetectionClickCommand;
		private ICommand _buttonTakePictureClickCommand;
		private ICommand _buttonOpenSettingsClickCommand;

		public ICommand KeyDownObjectDetectionCommand => _keyDownObjectDetectionCommand ?? (_keyDownObjectDetectionCommand = new DelegateCommand(BeginObjectDetection));
		public ICommand ButtonConnectWebcamClickCommand => _buttonConnectWebcamClickCommand ?? (_buttonConnectWebcamClickCommand = new DelegateCommand(ConnectToWebcam));
		public ICommand ButtonStartObjectDetectionClickCommand => _buttonStartObjectDetectionClickCommand ?? (_buttonStartObjectDetectionClickCommand = new DelegateCommand(BeginObjectDetection));
		public ICommand ButtonTakePictureClickCommand => _buttonTakePictureClickCommand ?? (_buttonTakePictureClickCommand = new DelegateCommand(TakePicture));
		public ICommand ButtonOpenSettingsClickCommand => _buttonOpenSettingsClickCommand ?? (_buttonOpenSettingsClickCommand = new DelegateCommand(ShowSettingsWindow));

		/// <summary>
		/// Starts the object detection if a webcam is connected or a picture is chosen from the disk of the PC, otherwise a messagebox with an indication for the user is shown.
		/// While starting the object detection the content of the responsible button is changed as asynchronous Task.
		/// If the image is from the disk it will be used for the object detection, otherwise a picture is taken with the webcam and the picture is used for the object detection.
		/// </summary>
		/// <returns>Returns the Task that is responsible for changing the text for the button to show the object detection is executing.</returns>
		private async Task StartObjectDetection()
		{
			//if the webcam has been connected or the user has choosen an image from disk
			if (_camera.IsConnected() || LiveVideo != null)
			{
				await UpdateObjectDetectionButtonAsTask(Properties.Resources.Processing); //processing
				string imagePath;

				if (_isImageFromDisk)
				{
					imagePath = _imageFromDisk;
				}
				else
				{
					var absoluteFilteredImagePath = SaveImage();
					imagePath = absoluteFilteredImagePath;
				}

				PredictImageFromPath(imagePath);

				await UpdateObjectDetectionButtonAsTask(Properties.Resources.StartObjectDetection); //processing stopped
			}
			else
			{
				MessageBox.Show(Properties.Resources.NoObjectDetectionPossibleContent, Properties.Resources.NoObjectDetectionPossibleHeader, MessageBoxButton.OK, MessageBoxImage.Warning);
			}
		}

		/// <summary>
		/// Executes the object detection and hands over the file path of the used image as parameter to the object detection algorithm.
		/// If the prediction result doesn't contain any errors, the chunked image with colored border is read and set, so it is shown on the right side of the GUI.
		/// In the end the prediction result is processed with the Text-To-Speech algorithm.
		/// </summary>
		/// <param name="absoluteFilteredImagePath">Filepath of the image that is used for the object detection.</param>
		private void PredictImageFromPath(string absoluteFilteredImagePath)
		{
			PythonConnector pythonConnector = new PythonConnector();
			string prediction = pythonConnector.GetPrediction(absoluteFilteredImagePath);

			if (!prediction.Contains(Properties.Resources.Error))
			{
				var chunkedImage = WebcamHelper.GetBitmapImageFromSource(Properties.Resources.ChunkedImagePath);
				SetImageSource(chunkedImage);
			}

			PredictionTextToSpeech(prediction);
		}

		/// <summary>
		/// Text-To-Speech algorithm is used to output the given prediction if the Text-To-Speech setting is enabled.
		/// </summary>
		/// <param name="prediction">Prediction result string that contains the values, probabilities and number of elements.</param>
		private void PredictionTextToSpeech(string prediction)
		{
			if (new SettingsController().GetTextToSpeech())
			{
				TextToSpeech textToSpeech = new TextToSpeech();
				textToSpeech.InvokeAsyncTextToSpeech(prediction);
			}
		}

		/// <summary>
		/// Uses the current frame of the webcam and saves it to the images folder.
		/// The location of the saved image is returned.
		/// </summary>
		/// <returns>Absolute filepath of the saved image from webcam.</returns>
		private string SaveImage()
		{
			var picture = _camera.GetBitmap();
			var absolutePath = WebcamHelper.TakePicture(picture);
			return absolutePath;
		}

		/// <summary>
		/// Sets the ImageSource of the LiveImage to the given bitmap image.
		/// </summary>
		/// <param name="image">Image of type bitmap that is set as ImageSource.</param>
		private void SetImageSource(Bitmap image)
		{
			var webcamFrame = WebcamHelper.ImageSourceForBitmap(image);
			LiveImage = webcamFrame;
		}

		/// <summary>
		/// Updates the content text of the button that is responsible for the object detection.
		/// </summary>
		/// <param name="message">Mesage that is shown as content text of the button.</param>
		public void UpdateObjectDetectionButton(string message)
		{
			StartObjectDetectionButtonText = message;
		}

		/// <summary>
		/// Updates the content text of the button that is responsible for the object detection as asynchronous task with a 10 ms delay.
		/// </summary>
		/// <param name="message">Mesage that is shown as content text of the button.</param>
		/// <returns>Returns the Task that is responsible for changing the text for the button to show the object detection is executing.</returns>
		public async Task UpdateObjectDetectionButtonAsTask(string message)
		{
			UpdateObjectDetectionButton(message);
			await Task.Delay(10);
		}

		//call to avoid exception when closing the window without disconnecting the camera
		//private void Window_Closing(object sender, CancelEventArgs e)
		//{
		//	_backgroundWorker.CancelAsync();
		//}

		/// <summary>
		/// This method is Invoked when the KeyDownObjectDetectionCommand (keypress "P") or the ButtonStartObjectDetectionClickCommand (button for object detection was clicked) is executed.
		/// Starts the object detection. 
		/// </summary>
		/// <param name="obj">Optional command parameter.</param>
		private async void BeginObjectDetection(object obj)
		{
			await StartObjectDetection();
		}

		/// <summary>
		/// This method is Invoked when the ButtonConnectWebcamClickCommand (button for connecting the webcam was clicked) is executed.
		/// If the camera is not connected, a connection is established and the backgroundworker begins to run.
		/// Otherwise the backgroundworker is stopped. If there couldn't be established a connection to the webcam, user feedback is shown. 
		/// </summary>
		/// <param name="obj">Optional command parameter.</param>
		private void ConnectToWebcam(object obj)
		{
			try
			{
				if (!_camera.IsConnected())
				{
					_camera.Connect();
					ConnectButtonText = Properties.Resources.DisconnectWebcam;
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
				MessageBox.Show(Properties.Resources.NoConnectionMessage, Properties.Resources.Attention, MessageBoxButton.OK, MessageBoxImage.Warning);
			}
		}

		/// <summary>
		/// This method is Invoked when the ButtonTakePictureClickCommand is executed. 
		/// User chooses image from disk which is used for object detection.
		/// If the button for choosing the image is clicked, an open file dialog opens from which the user can choose the image which is used for object detection. 
		/// The image is displayed on the left side of the gui (live webcam video). The result is displayed on the right side of the gui.
		/// </summary>
		/// <param name="obj">Optional parameter for command.</param>
		private void TakePicture(object obj)
		{
			try
			{
				OpenFileDialog openFileDialog =
					new OpenFileDialog { Filter = Properties.Resources.ImageFilterOpenFileDialog };

				if (openFileDialog.ShowDialog() == true)
				{
					string fileName = openFileDialog.FileName;
					LiveVideo = new BitmapImage(new Uri(fileName));
					_imageFromDisk = fileName;
				}

				_isImageFromDisk = true;

			}
			catch (FileFormatException fileFormatException)
			{
				Logger.Log(fileFormatException.Message);
			}
		}

		/// <summary>
		///	This method is Invoked when the ButtonOpenSettingsClickCommand is executed.
		/// Opens a new settings window.  
		/// </summary>
		/// <param name="obj">Optional parameter for command.</param>
		private void ShowSettingsWindow(object obj)
		{
			new SettingsWindow().Show();
		}

		/// <summary>
		/// Is invoked when the progress of the backgroundworker changed.
		/// Sets the LiveVideo of the webcam every frame and logs occuring errors.
		/// </summary>
		/// <param name="sender">Control that invoked the event.</param>
		/// <param name="progressChangedEventArgs">Event arguments that hold information about the process.</param>
		private void BackgroundWorkerOnProgressChanged(object sender, ProgressChangedEventArgs progressChangedEventArgs)
		{
			try
			{
				LiveVideo = progressChangedEventArgs.UserState as ImageSource;
			}
			catch (Exception e)
			{
				Logger.Log(e.Message);
			}
		}

		/// <summary>
		/// Is invoked when the backgroundworker stopped.
		/// Webcam is disconnected.
		/// </summary>
		/// <param name="sender">Control that invoked the event.</param>
		/// <param name="e">Event argmuents that hold information about the process.</param>
		private void Worker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
		{
			try
			{
				_camera.Disconnect();
				ConnectButtonText = Properties.Resources.ConnectWebcam;

				LiveVideo = new BitmapImage(new Uri(Properties.Resources.NoCameraUri));
			}
			catch (Exception exception)
			{
				Logger.Log(exception.Message);
			}
		}


		/// <summary>
		/// Is invoked while the backgroundworker is doing work.
		/// Updates the webcam frames and invokes the ProgressChangedEvent of the backgroundworker to set the new frame.
		/// </summary>
		/// <param name="sender">Control that invoked the event.</param>
		/// <param name="e">Event argmuents that hold information about the process.</param>
		private void Worker_DoWork(object sender, DoWorkEventArgs e)
		{
			while (!_backgroundWorker.CancellationPending)
			{
				try
				{
					_camera.Update();

					//convert camera image (bitmap) to imagesource that is freezable (fixed image) 
					Freezable webcamFrame = WebcamHelper.ImageSourceForBitmap(_camera.CalcBitmap()).GetAsFrozen();

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
					LiveVideo.Dispatcher.Invoke(UpdateWebCamVideoImageSource);
				}
				catch (Exception exception)
				{
					//log problems using the camera
					Logger.Log(exception.Message);
				}
			}
		}
	}
}
