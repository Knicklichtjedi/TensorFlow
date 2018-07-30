
namespace Traicy.GUI.Data
{
	/// <summary>
	/// Data class that represents all settings wrapped as settings model (gui, image, filter and loading).
	/// </summary>
	public class SettingProperties {

		[Newtonsoft.Json.JsonProperty(PropertyName = "image")]
        public ImageSettings ImageSettings { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "filter")]
        public FilterSettings FilterSettings { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "gui")]
        public GuiSettings GuiSettings { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "loading")]
        public LoadingSettings LoadingSettings { get; set; }
    }
}
