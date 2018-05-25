using System.Collections.Generic;
using Traicy.GUI.Contracts;

namespace Traicy.GUI.Data
{
    public class GuiSettings : IGuiSettings
    {
        [Newtonsoft.Json.JsonProperty(PropertyName = "text_to_speech_enabled")]
        public bool TextToSpeechIsEnabled { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "show_filtered_images_enabled")]
        public bool ShowFilteredImagesIsEnabled { get; set; }
        //[Newtonsoft.Json.JsonProperty(PropertyName = "filtered_images")]
        //public List<FilteredImages> FilteredImages { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "python_interpreter_path")]
        public string PythonInterpreterPath { get; set; }
    }
}
