using Traicy.GUI.Contracts;

namespace Traicy.GUI.Data
{
    public class GuiSettings : IGuiSettings
    {
        [Newtonsoft.Json.JsonProperty(PropertyName = "text_to_speech_enabled")]
        public bool TextToSpeechIsEnabled { get; set; }
    }
}
