using System.Collections.Generic;
using Traicy.GUI.Contracts;
using Traicy.GUI.Data;

namespace Traicy.GUI.Logic
{
    public class SettingsController
    {
        public ISettingProperties CreateJsonFileWithStandardValues()
        {
            FilterSettings filter = new FilterSettings()
            {
                Canny = 0.5f,
                BinaryGauss = 0.5f,
                BinaryThreshold = 0.5f,
                GreenBrightness = 0.25f,
                GreenHigh = 170,
                GreenLow = 50,
                GreenSaturation = 0.5f,
                MinimalOutlineSizeChunking = 90000,
                Schmiering = 2,
                ChunkBorder = 5
            };

            GuiSettings guiSettings = new GuiSettings { TextToSpeechIsEnabled = true, ShowFilteredImagesIsEnabled = true, PythonInterpreterPath = @"C:\Users\Eva\Anaconda3\envs\customTFLearn\python.exe" };

            ImageSettings imageSettings = new ImageSettings { Border = 2, Dimension = 28, DimensionSmall = 27 };

            List<string> loadingPictureStrings = new List<string> { "png", "jpg"};
            LoadingSettings loadingSettings = new LoadingSettings {PossibleImageFileTypes = loadingPictureStrings};

            ISettingProperties settingsProperties = new SettingProperties
            {
                FilterSettings = filter,
                ImageSettings = imageSettings,
                GuiSettings = guiSettings,
                LoadingSettings = loadingSettings
            };

            JsonParser.SerializeToJson(settingsProperties, @"configs\settings.json");

            return settingsProperties;
        }

    }
}
