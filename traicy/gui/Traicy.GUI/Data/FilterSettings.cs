using Traicy.GUI.Contracts;

namespace Traicy.GUI.Data
{
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
        [Newtonsoft.Json.JsonProperty(PropertyName = "schmiering")]
        public float Schmiering { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "min_chunk_size")]
        public float MinimalOutlineSizeChunking { get; set; }
    }
}
