using System.IO;
using System.Linq;
using System.Text;

namespace Traicy.GUI.Logic
{
	/// <summary>
	/// Class that acts as layer between this program and the python processing.
	/// </summary>
    public class PythonConnector
    {
		/// <summary>
		/// Returns the prediction for the image from the given filepath.
		/// </summary>
		/// <param name="absoluteImagePath"></param>
		/// <returns></returns>
        public string GetPrediction(string absoluteImagePath)
        {
            var result = new ObjectDetection().InvokeObjectDetection(absoluteImagePath);
	        return ParseResult(result);
        }

		/// <summary>
		/// Parses the result string to an output string for the Text-To-Speech algorithm. 
		/// Customizes the output string in dependency of the number of list elements. 
		/// It is differentiated between no result, one result element, more than one result elements and occuring errors.s
		/// </summary>
		/// <param name="result">The result string from object detection which contains the values and the probabilities.</param>
		/// <returns>Parsed string that contains the prediction with value(s), the probability/ies and the number of elements.</returns>
		private string ParseResult(string result)
	    {
			if (!string.IsNullOrEmpty(result))
			{
				var parsedPrediction = PythonOutputParser.ParseToListOfPredictions(result);

				StringBuilder stringBuilder = new StringBuilder();

				if (parsedPrediction.Count == 0)
				{
					stringBuilder.Append(Properties.Resources.NoResultFound);
					return stringBuilder.ToString();
				}
				if (parsedPrediction.Count == 1)
				{
					bool isNumber = Directory.GetDirectories(Properties.Resources.PythonModelPath).Any(d => d.Contains(Properties.Resources.ModelNumber));
					//bool isNumber = Directory.EnumerateFiles(Properties.Resources.PythonModelPath).Any(f => f.Contains(Properties.Resources.MNIST));
					stringBuilder.Append(isNumber ? Properties.Resources.FoundNumber : Properties.Resources.FoundLetter);

					var number = parsedPrediction[0].PredictedValue;
					var probability = parsedPrediction[0].PredictionPercentage;
					stringBuilder.Append(number);
					stringBuilder.Append(Properties.Resources.Probability);
					stringBuilder.Append(probability);
					stringBuilder.Append(Properties.Resources.Percent);
					stringBuilder.Append(Properties.Resources.Comma);
				}
				else if (parsedPrediction.Count >= 2)
				{

					stringBuilder.Append(Properties.Resources.FoundTheFollowing);

					string numberOfChunksFound = parsedPrediction.Count.ToString();
					stringBuilder.Append(numberOfChunksFound);

					bool isNumber = Directory.EnumerateFiles(Properties.Resources.PythonModelPath).Any(f => f.Contains(Properties.Resources.MNIST));
					stringBuilder.Append(isNumber ? Properties.Resources.FoundNumbers : Properties.Resources.FoundLetters);

					foreach (var pred in parsedPrediction)
					{
						var number = pred.PredictedValue;
						var probability = pred.PredictionPercentage;

						stringBuilder.Append(number);
						stringBuilder.Append(Properties.Resources.Probability);
						stringBuilder.Append(probability);
						stringBuilder.Append(Properties.Resources.Percent);
						stringBuilder.Append(Properties.Resources.Comma);
					}

					stringBuilder.Append(Properties.Resources.ThatIsAll);
				}

				stringBuilder.Append(Properties.Resources.ThatIsAll);

				return stringBuilder.ToString();
			}
			return Properties.Resources.ThereHasBeenAnError;
		}
    }
}
