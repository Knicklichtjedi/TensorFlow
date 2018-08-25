namespace Traicy.GUI.Data
{
	/// <summary>
	/// Data class that represents all user interface settings in the JSON settings file.
	/// </summary>
	public class GuiSettings
    {
        [Newtonsoft.Json.JsonProperty(PropertyName = "text_to_speech_enabled")]
        public bool TextToSpeechIsEnabled { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "python_interpreter_path")]
        public string PythonInterpreterPath { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "tf_model_mode")]
        public string TfModelMode { get; set; }
    }
}
