using System.Windows;
using Traicy.GUI.Contracts;

namespace Traicy.GUI.View
{
    /// <summary>
    /// Interaktionslogik für SettingsWindow.xaml
    /// </summary>
    public partial class SettingsWindow : Window
    {
        public SettingsWindow()
        {
            InitializeComponent();
        }

        public SettingsWindow(ISettingProperties settingProperties)
        {
            InitializeComponent();

            SettingsUserControl.InitializeSettings(settingProperties);
        }
    }
}
