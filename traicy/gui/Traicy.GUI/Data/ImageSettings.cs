namespace Traicy.GUI.Data
{
	/// <summary>
	/// Data class that represents all python image settings in the JSON settings file.
	/// </summary>
	public class ImageSettings
	{
		[Newtonsoft.Json.JsonProperty(PropertyName = "dimension")]
		public int Dimension { get; set; }
		[Newtonsoft.Json.JsonProperty(PropertyName = "dimension_small")]
		public int DimensionSmall { get; set; }
		[Newtonsoft.Json.JsonProperty(PropertyName = "border")]
		public int Border { get; set; }
	}
}
