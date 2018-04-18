using Traicy.GUI.Contracts;

namespace Traicy.GUI.Data
{
    public class SettingProperties : ISettingProperties
    {

        [Newtonsoft.Json.JsonProperty(PropertyName = "image")]
        public ImageSettings ImageSettings { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "filter")]
        public FilterSettings FilterSettings { get; set; }
        //[Newtonsoft.Json.JsonProperty(PropertyName = "gui")]
        //public GuiSettings GuiSettings { get; set; }
    }
}
