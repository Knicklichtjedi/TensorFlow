using System;
using System.ComponentModel;
using System.Globalization;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
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

        public SettingsControl()
        {
            InitializeComponent();

            if (!DesignerProperties.GetIsInDesignMode(this))
            {
            
            _textToSpeechEnabled = true;
            ISettingProperties settings = JsonParser.DeserializeFromJson<SettingProperties>("settingsTest.json");

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
    }

        private void ToggleSpeechButton_OnClick(object sender, RoutedEventArgs e)
        {
            if (sender != null)
            {
                if (sender is ToggleButton button)
                {
                    //toggle between 
                    _textToSpeechEnabled = !_textToSpeechEnabled;
                    EventHandling.OnTextToSpeechEvent(_textToSpeechEnabled);
                    button.Content = _textToSpeechEnabled ? "An" : "Aus";
                }
            }
        }

        private void SaveSettingsButton_OnClick(object sender, RoutedEventArgs e)
        {
            var settings = GetSettingPropertiesFromSettings();
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

            //IGuiSettings guiSettings = new GuiSettings() { TextToSpeechIsEnabled = true };

            ImageSettings imageSettings = new ImageSettings()
            {
                Border = Convert.ToInt32(BorderTextBox.Text),
                Dimension = Convert.ToInt32(DimensionTextBox.Text),
                DimensionSmall = Convert.ToInt32(DimensionSmallTextBox.Text)
            };

            SettingProperties settingsProperties = new SettingProperties
            {
                FilterSettings = filter,
                ImageSettings = imageSettings
            };

            return settingsProperties;
        }
    }
}
