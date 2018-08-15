using System;
using System.Globalization;
using System.Windows.Input;
using Microsoft.Win32;
using Traicy.GUI.Commands;
using Traicy.GUI.Contracts;
using Traicy.GUI.Data;
using Traicy.GUI.Logic;

namespace Traicy.GUI.ViewModels
{
	class SettingsViewModel : ViewModelBase
	{
		public SettingsViewModel()
		{
			InitializeSettings();
		}

		private SettingProperties _jsonSettingsModel;

		/*-------------------------gui settings--------------------------*/
		private string _textToSpeechEnabled;
		public string TextToSpeechEnabled
		{
			get => _textToSpeechEnabled;
			set
			{
				if (_textToSpeechEnabled == value)
					return;
				_textToSpeechEnabled = value;
				OnPropertyChanged(nameof(TextToSpeechEnabled));
			}
		}

		private string _pythonInterpreterText;
		public string PythonInterpreterText
		{
			get => _pythonInterpreterText;
			set
			{
				if (_pythonInterpreterText == value)
					return;
				_pythonInterpreterText = value;
				OnPropertyChanged(nameof(PythonInterpreterText));
			}
		}

        private string _tfModelMode;
        public string TFModelMode
        {
            get => _tfModelMode;
            set
            {
                if (_tfModelMode == value)
                    return;
                _tfModelMode = value;
                OnPropertyChanged(nameof(TFModelMode));
            }
        }

        /*-------------------------image settings--------------------------*/
        private string _dimensionText;
		public string DimensionText
		{
			get => _dimensionText;
			set
			{
				if (_dimensionText == value)
					return;
				_dimensionText = value;
				OnPropertyChanged(nameof(DimensionText));
				_jsonSettingsModel.ImageSettings.Dimension = Convert.ToInt32(_dimensionText);
				SettingsHaveBeenSaved = false;
			}
		}

		private string _dimensionSmallText;
		public string DimensionSmallText
		{
			get => _dimensionSmallText;
			set
			{
				if (_dimensionSmallText == value)
					return;
				_dimensionSmallText = value;
				OnPropertyChanged(nameof(DimensionSmallText));
				_jsonSettingsModel.ImageSettings.DimensionSmall = Convert.ToInt32(_dimensionSmallText);
				SettingsHaveBeenSaved = false;
			}
		}

		private string _borderText;
		public string BorderText
		{
			get => _borderText;
			set
			{
				if (_borderText == value)
					return;
				_borderText = value;
				OnPropertyChanged(nameof(BorderText));
				_jsonSettingsModel.ImageSettings.Border = Convert.ToInt32(_borderText);
				SettingsHaveBeenSaved = false;
			}
		}

		/*-------------------------filter settings--------------------------*/
		private string _cannyText;
		public string CannyText
		{
			get => _cannyText;
			set
			{
				if (_cannyText == value)
					return;
				_cannyText = value;
				OnPropertyChanged(nameof(CannyText));
				_jsonSettingsModel.FilterSettings.Canny = Convert.ToSingle(_cannyText);
				SettingsHaveBeenSaved = false;
			}
		}

		private string _binaryGaussText;
		public string BinaryGaussText
		{
			get => _binaryGaussText;
			set
			{
				if (_binaryGaussText == value)
					return;
				_binaryGaussText = value;
				OnPropertyChanged(nameof(BinaryGaussText));
				_jsonSettingsModel.FilterSettings.BinaryGauss = Convert.ToSingle(_binaryGaussText);
				SettingsHaveBeenSaved = false;
			}
		}

		private string _binaryThresholdText;
		public string BinaryThresholdText
		{
			get => _binaryThresholdText;
			set
			{
				if (_binaryThresholdText == value)
					return;
				_binaryThresholdText = value;
				OnPropertyChanged(nameof(BinaryThresholdText));
				_jsonSettingsModel.FilterSettings.BinaryThreshold = Convert.ToSingle(_binaryThresholdText);
				SettingsHaveBeenSaved = false;
			}
		}

		private string _greenLowText;
		public string GreenLowText
		{
			get => _greenLowText;
			set
			{
				if (_greenLowText == value)
					return;
				_greenLowText = value;
				OnPropertyChanged(nameof(GreenLowText));
				_jsonSettingsModel.FilterSettings.GreenLow = Convert.ToInt32(_greenLowText);
				SettingsHaveBeenSaved = false;
			}
		}

		private string _greenHighText;
		public string GreenHighText
		{
			get => _greenHighText;
			set
			{
				if (_greenHighText == value)
					return;
				_greenHighText = value;
				OnPropertyChanged(nameof(GreenHighText));
				_jsonSettingsModel.FilterSettings.GreenHigh = Convert.ToInt32(_greenHighText);
				SettingsHaveBeenSaved = false;
			}
		}

		private string _greenSaturationText;
		public string GreenSaturationText
		{
			get => _greenSaturationText;
			set
			{
				if (_greenSaturationText == value)
					return;
				_greenSaturationText = value;
				OnPropertyChanged(nameof(GreenSaturationText));
				_jsonSettingsModel.FilterSettings.GreenSaturation = Convert.ToSingle(_greenSaturationText);
				SettingsHaveBeenSaved = false;
			}
		}

		private string _greenBrightnessText;
		public string GreenBrightnessText
		{
			get => _greenBrightnessText;
			set
			{
				if (_greenBrightnessText == value)
					return;
				_greenBrightnessText = value;
				OnPropertyChanged(nameof(GreenBrightnessText));
				_jsonSettingsModel.FilterSettings.GreenBrightness = Convert.ToSingle(_greenBrightnessText);
				SettingsHaveBeenSaved = false;
			}
		}

		private string _schmieringText;
		public string SchmieringText
		{
			get => _schmieringText;
			set
			{
				if (_schmieringText == value)
					return;
				_schmieringText = value;
				OnPropertyChanged(nameof(SchmieringText));
				_jsonSettingsModel.FilterSettings.Schmiering = Convert.ToInt32(_schmieringText);
				SettingsHaveBeenSaved = false;
			}
		}

		private string _minOutlineSizeText;
		public string MinOutlineSizeText
		{
			get => _minOutlineSizeText;
			set
			{
				if (_minOutlineSizeText == value)
					return;
				_minOutlineSizeText = value;
				OnPropertyChanged(nameof(MinOutlineSizeText));
				_jsonSettingsModel.FilterSettings.MinimalOutlineSizeChunking = Convert.ToInt32(_minOutlineSizeText);
				SettingsHaveBeenSaved = false;
			}
		}

		private string _chunkBorderText;
		public string ChunkBorderText
		{
			get => _chunkBorderText;
			set
			{
				if (_chunkBorderText == value)
					return;
				_chunkBorderText = value;
				OnPropertyChanged(nameof(ChunkBorderText));
				_jsonSettingsModel.FilterSettings.ChunkBorder = Convert.ToInt32(_chunkBorderText);
				SettingsHaveBeenSaved = false;
			}
		}

		/*-------------------------loading settings--------------------------*/
		private string _loadingFileExtensionForImagesText;
		public string LoadingFileExtensionForImagesText
		{
			get => _loadingFileExtensionForImagesText;
			set
			{
				if (_loadingFileExtensionForImagesText == value)
					return;
				_loadingFileExtensionForImagesText = value;
				OnPropertyChanged(nameof(LoadingFileExtensionForImagesText));
				_jsonSettingsModel.LoadingSettings.PossibleImageFileTypes = PythonOutputParser.ParseStringToList(_loadingFileExtensionForImagesText);
				SettingsHaveBeenSaved = false;
			}
		}

		private bool _settingsHaveBeenSaved;
		public bool SettingsHaveBeenSaved
		{
			get => _settingsHaveBeenSaved;
			set
			{
				if (_settingsHaveBeenSaved == value)
					return;
				_settingsHaveBeenSaved = value;
				OnPropertyChanged(nameof(SettingsHaveBeenSaved));
			}
		}

		/*-------------------------commands--------------------------*/
		private ICommand _toggleSpeechButtonClickCommand;
		private ICommand _choosePythonInterpreterButtonClickCommand;
		private ICommand _toggleTFModelButtonClickCommand;
		private ICommand _saveSettingsButtonClickCommand;

		public ICommand ToggleSpeechButtonClickCommand => _toggleSpeechButtonClickCommand ?? (_toggleSpeechButtonClickCommand = new DelegateCommand(ClickToggleSpeechButton));
		public ICommand ChoosePythonInterpreterButtonClickCommand => _choosePythonInterpreterButtonClickCommand ?? (_choosePythonInterpreterButtonClickCommand = new DelegateCommand(ChoosePythonInterpreterButton));
		public ICommand ToggleTFModelButtonClickCommand => _toggleTFModelButtonClickCommand ?? (_toggleTFModelButtonClickCommand = new DelegateCommand(ClickTFModelModeButton));
        public ICommand SaveSettingsButtonClickCommand => _saveSettingsButtonClickCommand ?? (_saveSettingsButtonClickCommand = new DelegateCommand(SaveSettings));

		/// <summary>
		/// Sets (and converts if necessary) all settings loaded from the settings model to each of the binded properties of the view so that the settings are displayed in the settings window.
		/// </summary>
		private void InitializeSettings()
		{
			_jsonSettingsModel = new SettingsController().GetSettings();

			//set gui settings
			TextToSpeechEnabled = PythonOutputParser.ParseToString(_jsonSettingsModel.GuiSettings.TextToSpeechIsEnabled);
			TFModelMode = _jsonSettingsModel.GuiSettings.TFModelMode;
			PythonInterpreterText = _jsonSettingsModel.GuiSettings.PythonInterpreterPath;

			//set image settings
			DimensionText = _jsonSettingsModel.ImageSettings.Dimension.ToString();
			DimensionSmallText = _jsonSettingsModel.ImageSettings.DimensionSmall.ToString();
			BorderText = _jsonSettingsModel.ImageSettings.Border.ToString();

			//set filter settings
			CannyText = _jsonSettingsModel.FilterSettings.Canny.ToString(CultureInfo.CurrentCulture);
			BinaryGaussText = _jsonSettingsModel.FilterSettings.BinaryGauss.ToString(CultureInfo.CurrentCulture);
			BinaryThresholdText = _jsonSettingsModel.FilterSettings.BinaryThreshold.ToString(CultureInfo.CurrentCulture);
			GreenLowText = _jsonSettingsModel.FilterSettings.GreenLow.ToString(CultureInfo.CurrentCulture);
			GreenHighText = _jsonSettingsModel.FilterSettings.GreenHigh.ToString(CultureInfo.CurrentCulture);
			GreenSaturationText = _jsonSettingsModel.FilterSettings.GreenSaturation.ToString(CultureInfo.CurrentCulture);
			GreenBrightnessText = _jsonSettingsModel.FilterSettings.GreenBrightness.ToString(CultureInfo.CurrentCulture);
			SchmieringText = _jsonSettingsModel.FilterSettings.Schmiering.ToString(CultureInfo.CurrentCulture);
			MinOutlineSizeText = _jsonSettingsModel.FilterSettings.MinimalOutlineSizeChunking.ToString(CultureInfo.CurrentCulture);
			ChunkBorderText = _jsonSettingsModel.FilterSettings.ChunkBorder.ToString(CultureInfo.CurrentCulture);

			//set loading settings
			LoadingFileExtensionForImagesText = PythonOutputParser.ParseListToString(_jsonSettingsModel.LoadingSettings.PossibleImageFileTypes);

			//Set status of settings 
			SettingsHaveBeenSaved = false;
		}

		/// <summary>
		/// This method is Invoked when the ChoosePythonInterpreterButtonClickCommand is executed.
		/// An open file dialog is opened. The filename of the chosen path (of the python.exe) is set as new PythonInterpreterPath.
		/// </summary>
		/// <param name="obj">Optional command parameter.</param>
		private void ChoosePythonInterpreterButton(object obj)
		{
			OpenFileDialog openFileDialog =
				new OpenFileDialog { Filter = Properties.Resources.FileExtensionsInterpreter };
			if (openFileDialog.ShowDialog() == true)
			{
				PythonInterpreterText = openFileDialog.FileName;
				_jsonSettingsModel.GuiSettings.PythonInterpreterPath = PythonInterpreterText;
				SettingsHaveBeenSaved = false;
			}
		}

        /// <summary>
        /// 
        /// </summary>
        /// <param name="obj"></param>
        private void ClickTFModelModeButton(object obj)
        {
            var isEnabled = (bool)obj;
            //toggle between 
            TFModelMode = PythonOutputParser.ParseToModelMode(isEnabled);
            _jsonSettingsModel.GuiSettings.TFModelMode = TFModelMode;
            SettingsHaveBeenSaved = false;
        }

        /// <summary>
        /// This method is Invoked when the ToggleSpeechButtonClickCommand is executed.
        /// Sets the Text-To-Speech setting according to the status of the TextToSpeechButton in the settings window.
        /// </summary>
        /// <param name="obj">Command parameter that indicates whether the Text-To-Speech setting is enabled or disabled.</param>
        private void ClickToggleSpeechButton(object obj)
		{
			var isEnabled = (bool) obj;
			//toggle between 
			TextToSpeechEnabled = PythonOutputParser.ParseToString(isEnabled);
			_jsonSettingsModel.GuiSettings.TextToSpeechIsEnabled = isEnabled;
			SettingsHaveBeenSaved = false;
		}

		/// <summary>
		/// This method is Invoked when the SaveSettingsButtonClickCommand is executed.
		/// Settings are saved to the JSON file and sets the information that the settings were saved to true.
		/// </summary>
		/// <param name="obj">Optional command parameter.</param>
		private void SaveSettings(object obj)
		{
			new SettingsController().SaveSettingsToJsonFile(_jsonSettingsModel);
			SettingsHaveBeenSaved = true;
		}
	}
}
