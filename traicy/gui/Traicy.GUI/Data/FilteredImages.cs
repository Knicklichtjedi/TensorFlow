using System.Windows.Media;

namespace Traicy.GUI.Data
{
    public class FilteredImages
    {
        public ImageSource BinaryImage { get; set; }
        public ImageSource SkeletonImage { get; set; }

        [Newtonsoft.Json.JsonProperty(PropertyName = "binary_image_enabled")]
        public bool BinaryImageIsEnabled { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "skeleton_image_enabled")]
        public bool SkeletonImageIsEnabled { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName = "scaled_image_enabled")]
        public bool ScaledImageIsEnabled { get; set; }
        //TODO: weitere?
    }
}
