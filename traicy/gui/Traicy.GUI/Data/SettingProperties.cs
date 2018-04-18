using Traicy.GUI.Contracts;

namespace Traicy.GUI.Data
{
    public class SettingProperties : ISettingProperties
    {
        public ImageSettings ImageSettings { get; set; }
        public FilterSettings FilterSettings { get; set; }
        //public GuiSettings GuiSettings { get; set; }
    }
}
