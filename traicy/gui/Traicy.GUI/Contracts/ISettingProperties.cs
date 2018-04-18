using Traicy.GUI.Data;

namespace Traicy.GUI.Contracts
{
    public interface ISettingProperties
    {
        ImageSettings ImageSettings { get; set; }
        FilterSettings FilterSettings { get; set; }
        //IGuiSettings GuiSettings { get; set; }
    }
}
