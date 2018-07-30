using System.Collections.Generic;

namespace Traicy.GUI.Data
{
	/// <summary>
	/// Data class that represents all python loading settings (which image files are usable for object detection) in the JSON settings file.
	/// </summary>
	public class LoadingSettings
    {
        [Newtonsoft.Json.JsonProperty(PropertyName = "possible_filename")]
        public List<string> PossibleImageFileTypes { get; set; }
    }
}
