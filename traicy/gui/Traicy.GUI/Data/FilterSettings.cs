namespace Traicy.GUI.Data
{
	/// <summary>
	/// Data class that represents all python filter settings in the JSON settings file.
	/// </summary>
    public class FilterSettings
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
        public int Schmiering { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "contours_length")]
        public int MinimalOutlineSizeChunking { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "chunk_border")]
        public int ChunkBorder { get; set; }
    }
}
