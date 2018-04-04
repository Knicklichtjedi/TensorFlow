using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;

namespace Traicy.GUI.View
{
    /// <summary>
    /// Interaktionslogik für SettingsControl.xaml
    /// </summary>
    public partial class SettingsControl : UserControl
    {
        public SettingsControl()
        {
            InitializeComponent();
        }

        private void ToggleSpeechButton_OnClick(object sender, RoutedEventArgs e)
        {
            if (sender != null)
            {
                if (sender is ToggleButton button)
                {
                    button.Content = button.Content.ToString() == "An" ? "Aus" : "An";
                }

                //TODO: Sprachausgabe an- und ausschalten
            }
        }
    }
}
