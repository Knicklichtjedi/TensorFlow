namespace Traicy.GUI.Data
{
	/// <summary>
	/// Data class that represents the prediction that is the result of the object detection as detected value and confidence/probability.
	/// </summary>
	public class Prediction
    {
        public string PredictedValue { get; set; }
        public string PredictionPercentage { get; set; }
    }
}
