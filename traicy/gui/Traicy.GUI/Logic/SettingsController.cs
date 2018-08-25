using System.Collections.Generic;
using System.IO;
using Traicy.GUI.Data;

namespace Traicy.GUI.Logic
{
	/// <summary>
	/// Class that manages the loading and saving of the settings and the creation of a standard JSON setting file.
	/// </summary>
	public class SettingsController
	{
		//save settings when loaded
		public SettingProperties CachedSettings { get; private set; }

		/// <summary>
		/// Creates a new instance of SettingProperties with standard values for filter, image, gui and loading settings. Saves the standard settings to a new JSON settings file.
		/// </summary>
		/// <returns>SettingProperties with standard values for further use.</returns>
		private SettingProperties CreateJsonSettingsWithStandardValues()
		{
			FilterSettings filter = new FilterSettings
			{
				Canny = 0.5f,
				BinaryGauss = 0.5f,
				BinaryThreshold = 0.5f,
				GreenBrightness = 0.25f,
				GreenHigh = 170,
				GreenLow = 50,
				GreenSaturation = 0.5f,
				MinimalOutlineSizeChunking = 9000,
				Schmiering = 2,
				ChunkBorder = 5
			};

			GuiSettings guiSettings = new GuiSettings { TextToSpeechIsEnabled = true, PythonInterpreterPath = Properties.Resources.StandardPythonInterpreterPath, TfModelMode = Properties.Resources.ModelNumber };

			ImageSettings imageSettings = new ImageSettings { Border = 2, Dimension = 28, DimensionSmall = 26 };

			List<string> loadingPictureStrings = new List<string> { Properties.Resources.ImageTypePNG, Properties.Resources.ImageTypeJPG };
			LoadingSettings loadingSettings = new LoadingSettings { PossibleImageFileTypes = loadingPictureStrings };

			SettingProperties settingsProperties = new SettingProperties
			{
				FilterSettings = filter,
				ImageSettings = imageSettings,
				GuiSettings = guiSettings,
				LoadingSettings = loadingSettings
			};

			SaveSettingsToJsonFile(settingsProperties);

			return settingsProperties;
		}

		/// <summary>
		/// Creates a new directory named configs if it doesn't exist.
		/// </summary>
		private void CreateSettingsDirectory()
		{
			if (!Directory.Exists(Properties.Resources.JSONSettingsDirectoryName))
			{
				Directory.CreateDirectory(Properties.Resources.JSONSettingsDirectoryName);
			}
		}

		/// <summary>
		/// Loads the settings from the JSON file.
		/// </summary>
		/// <returns>All settings read from JSON file as SettingProperties</returns>
		private SettingProperties LoadSettingsFromJsonFile()
		{
			return JsonParser.DeserializeFromJson<SettingProperties>(Properties.Resources.JSONSettingsFilePath);
		}

		/// <summary>
		/// Writes the given settings to the JSON file and caches the settings.
		/// </summary>
		/// <param name="settings">Settings that are saved to the JSON file as SettingProperties</param>
		public void SaveSettingsToJsonFile(SettingProperties settings)
		{
			JsonParser.SerializeToJson(settings, Properties.Resources.JSONSettingsFilePath);
			CachedSettings = settings;
		}

		/// <summary>
		/// Returns the current settings and caches them. If a settings file already exists the settings will be loaded from it and are returned, 
		/// otherwise a new file will be created and standard values are returned.
		/// </summary>
		/// <returns>Cached settings.</returns>
		public SettingProperties GetSettings()
		{
			CreateSettingsDirectory();

			CachedSettings = !File.Exists(Properties.Resources.JSONSettingsFilePath) ? CreateJsonSettingsWithStandardValues() : LoadSettingsFromJsonFile();
			return CachedSettings;
		}

		/// <summary>
		/// Returns the python interpreter path from the cached settings or reads them if there aren't any cached settings.
		/// </summary>
		/// <returns>Python interpreter path as string.</returns>
		public string GetPythonInterpreterPath()
		{
			if (CachedSettings != null)
			{
				return CachedSettings.GuiSettings.PythonInterpreterPath;
			}
			return GetSettings().GuiSettings.PythonInterpreterPath;
		}

		/// <summary>
		/// Returns the information if Text-To-Speech is enabled from the cached settings or reads them if there aren't any cached settings.
		/// </summary>
		/// <returns>Information if Text-To-Speech is enabled.</returns>
		public bool GetTextToSpeech()
		{
			if (CachedSettings != null)
			{
				return CachedSettings.GuiSettings.TextToSpeechIsEnabled;
			}
			return GetSettings().GuiSettings.TextToSpeechIsEnabled;
		}

        /// <summary>
		/// Returns the information which TFModelMode is set from the cached settings or reads them if there aren't any cached settings.
		/// </summary>
		/// <returns>Information which TFModelMode is set as string.</returns>
        public string GetTfModelMode()
        {
            if (CachedSettings != null)
            {
                return CachedSettings.GuiSettings.TfModelMode;
            }
            return GetSettings().GuiSettings.TfModelMode;
        }
    }
}
