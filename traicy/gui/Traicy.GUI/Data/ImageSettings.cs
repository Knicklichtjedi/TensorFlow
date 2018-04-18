using Traicy.GUI.Contracts;

namespace Traicy.GUI.Data
{
    public class ImageSettings : IImageSettings
    {
        [Newtonsoft.Json.JsonProperty(PropertyName = "dimension")]
        public int Dimension { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "dimension_small")]
        public int DimensionSmall { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "border")]
        public int Border { get; set; }
    }
}
