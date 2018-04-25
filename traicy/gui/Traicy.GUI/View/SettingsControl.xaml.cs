using System;
using System.ComponentModel;
using System.Globalization;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using Microsoft.Win32;
using Traicy.GUI.Contracts;
using Traicy.GUI.Data;
using Traicy.GUI.Logic;

namespace Traicy.GUI.View
{
    /// <summary>
    /// Interaktionslogik für SettingsControl.xaml
    /// </summary>
    public partial class SettingsControl : UserControl
    {
        private bool _textToSpeechEnabled;
        private bool _filteredImagesEnabled;
        private string _pythonInterpreterPath;

        public SettingsControl()
        {
            InitializeComponent();

            if (!DesignerProperties.GetIsInDesignMode(this))
            {

                //_textToSpeechEnabled = true;
                //_filteredImagesEnabled = true;
                //ISettingProperties settings = JsonParser.DeserializeFromJson<SettingProperties>("settingsTest.json");

               //InitializeSettings(settings);
            }
        }

        public void InitializeSettings(ISettingProperties settings)
        {

            //set gui settings
            _textToSpeechEnabled = settings.GuiSettings.TextToSpeechIsEnabled;
            ButtonTextToSpeech.Content = _textToSpeechEnabled ? "An" : "Aus";

            _filteredImagesEnabled = settings.GuiSettings.ShowFilteredImagesIsEnabled;
            ButtonFilteredImages.Content = _filteredImagesEnabled ? "An" : "Aus";

            ChoosePythonInterpreterTextBox.Text = settings.GuiSettings.PythonInterpreterPath;

            //set image settings
            DimensionTextBox.Text = settings.ImageSettings.Dimension.ToString();
            DimensionSmallTextBox.Text = settings.ImageSettings.DimensionSmall.ToString();
            BorderTextBox.Text = settings.ImageSettings.Border.ToString();

            //set filter settings
            CannyTextBox.Text = settings.FilterSettings.Canny.ToString(CultureInfo.CurrentCulture);
            BinaryGaussTextBox.Text = settings.FilterSettings.BinaryGauss.ToString(CultureInfo.CurrentCulture);
            BinaryThresholdTextBox.Text = settings.FilterSettings.BinaryThreshold.ToString(CultureInfo.CurrentCulture);
            GreenLowTextBox.Text = settings.FilterSettings.GreenLow.ToString(CultureInfo.CurrentCulture);
            GreenHighTextBox.Text = settings.FilterSettings.GreenHigh.ToString(CultureInfo.CurrentCulture);
            GreenSaturationTextBox.Text = settings.FilterSettings.GreenSaturation.ToString(CultureInfo.CurrentCulture);
            GreenBrightnessTextBox.Text = settings.FilterSettings.GreenBrightness.ToString(CultureInfo.CurrentCulture);

        }

        private void ToggleSpeechButton_OnClick(object sender, RoutedEventArgs e)
        {
            if (sender != null)
            {
                if (sender is ToggleButton button)
                {
                    //toggle between 
                    _textToSpeechEnabled = !_textToSpeechEnabled;
                    //EventHandling.OnTextToSpeechEvent(_textToSpeechEnabled);
                    button.Content = _textToSpeechEnabled ? "An" : "Aus";
                }
            }
        }

        private void SaveSettingsButton_OnClick(object sender, RoutedEventArgs e)
        {
            var settings = GetSettingPropertiesFromSettings();
            EventHandling.OnSettingsChangedEvent(settings);
            JsonParser.SerializeToJson(settings, @"settingsTest.json");
            
        }

        private SettingProperties GetSettingPropertiesFromSettings()
        {
            FilterSettings filter = new FilterSettings
            {
                Canny = Convert.ToSingle(CannyTextBox.Text),
                BinaryGauss = Convert.ToSingle(BinaryGaussTextBox.Text),
                BinaryThreshold = Convert.ToSingle(BinaryThresholdTextBox.Text),
                GreenBrightness = Convert.ToSingle(GreenBrightnessTextBox.Text),
                GreenHigh = Convert.ToInt32(GreenHighTextBox.Text),
                GreenLow = Convert.ToInt32(GreenLowTextBox.Text),
                GreenSaturation = Convert.ToSingle(GreenSaturationTextBox.Text)
            };

            GuiSettings guiSettings = new GuiSettings()
            {
                TextToSpeechIsEnabled = _textToSpeechEnabled,
                PythonInterpreterPath = _pythonInterpreterPath,
                ShowFilteredImagesIsEnabled = _filteredImagesEnabled
            };

            ImageSettings imageSettings = new ImageSettings()
            {
                Border = Convert.ToInt32(BorderTextBox.Text),
                Dimension = Convert.ToInt32(DimensionTextBox.Text),
                DimensionSmall = Convert.ToInt32(DimensionSmallTextBox.Text)
            };

            SettingProperties settingsProperties = new SettingProperties
            {
                FilterSettings = filter,
                ImageSettings = imageSettings,
                GuiSettings = guiSettings
            };

            return settingsProperties;
        }

        private void ButtonFilteredImages_OnClick(object sender, RoutedEventArgs e)
        {
            if (sender != null)
            {
                if (sender is ToggleButton button)
                {
                    //toggle between 
                    _filteredImagesEnabled = !_filteredImagesEnabled;
                    //EventHandling.OnFilteredImagesEvent(_filteredImagesEnabled);
                    button.Content = _filteredImagesEnabled ? "An" : "Aus";
                }
            }
        }

        private void ChoosePythonInterpreterButton_OnClick(object sender, RoutedEventArgs e)
        {
            OpenFileDialog openFileDialog =
                new OpenFileDialog {Filter = "Executable files (*.exe)|*.exe|All files (*.*)|*.*"};
            if (openFileDialog.ShowDialog() == true)
            {
                _pythonInterpreterPath = openFileDialog.FileName;
                ChoosePythonInterpreterTextBox.Text = _pythonInterpreterPath;
            }

        }
    }
}
