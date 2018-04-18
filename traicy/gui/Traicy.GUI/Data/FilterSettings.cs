using Traicy.GUI.Contracts;

namespace Traicy.GUI.Data
{
    [Newtonsoft.Json.JsonObject(Title = "filter")]
    public class FilterSettings : IFilterSettings
    {
        [Newtonsoft.Json.JsonProperty(PropertyName = "canny")]
        public float Canny { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "binary_gauss")]
        public float BinaryGauss { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "binary_threshold")]
        public float BinaryThreshold { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "green_low")]
        public int GreenLow { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "green_high")]
        public int GreenHigh { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "green_saturation")]
        public float GreenSaturation { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "green_brightness")]
        public float GreenBrightness { get; set; }
    }
}
