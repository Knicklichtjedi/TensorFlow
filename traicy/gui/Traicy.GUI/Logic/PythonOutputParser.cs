using System;
using System.Collections.Generic;
using System.Linq;
using Traicy.GUI.Data;

namespace Traicy.GUI.Logic
{
	/// <summary>
	/// Converter class for several types that are used for object detection and processing in the view.
	/// </summary>
    public class PythonOutputParser
    {
		/// <summary>
		/// Converts a string to a string array by splitting its content at comma characters.
		/// </summary>
		/// <param name="toParse">String that contains commas as separators.</param>
		/// <returns>Split strings as array.</returns>
	    private static string[] Parse(string toParse)
	    {
		    var parsedStrings = toParse.Split(new[] { "," }, StringSplitOptions.RemoveEmptyEntries);
		    return parsedStrings;
	    }

		/// <summary>
		/// Converts a string to a Prediction that contains a prediction value and a prediction percentage.
		/// </summary>
		/// <param name="toParse">String that is parsed.</param>
		/// <returns>Prediction with prediction value and prediction percentage</returns>
		private static Prediction ParseToPrediction(string toParse)
	    {
		    var parsedLine = Parse(toParse);
            Prediction prediction = new Prediction
            {
                PredictedValue = parsedLine[0],
                PredictionPercentage = ParsePercentage(parsedLine[1])
		    };

		    return prediction;
	    }

        /// <summary>
        /// Formats a percentage value with the style "XX.XX" to "XX Komma X X" for the TTS integration. 
        /// </summary>
        /// <param name="toParse">Given string of the percentage to format.</param>
        /// <returns>The formatted string that contains the probability.</returns>
        private static string ParsePercentage(string toParse)
        {
            string[] splitted = toParse.Split('.');
            char[] postComma = splitted[1].ToCharArray();

            string stringForTTS = splitted[0] + " Komma";

            foreach(char c in postComma)
            {
                stringForTTS += " " + c;
            }

            return stringForTTS;
        }

        /// <summary>
        /// Converts a string to a list of strings. The string is split and parsed to a string array, which is converted into a list.
        /// </summary>
        /// <param name="toParse">String that is parsed.</param>
        /// <returns>A list of strings.</returns>
        public static List<string> ParseStringToList(string toParse)
        {
            var parsedLoadingString = Parse(toParse);

	        return parsedLoadingString.ToList();
        }

		/// <summary>
		/// Converts a list of strings to a string by concatenating the elements of the list with a comma.
		/// </summary>
		/// <param name="toParse">List of string that are parsed to a string.</param>
		/// <returns>Concatenated string.</returns>
		public static string ParseListToString(List<string> toParse)
        {
            string concatenatedFileExtensionStringForJsonSettingsSaving = String.Empty;
            for (int i = 0; i < toParse.Count; i++)
            {
                //if last element don't set comma
                if (i == toParse.Count - 1)
                {
                    concatenatedFileExtensionStringForJsonSettingsSaving += toParse[i];
                }
                else
                {
                    concatenatedFileExtensionStringForJsonSettingsSaving += $"{toParse[i]},";
                }
            }

            return concatenatedFileExtensionStringForJsonSettingsSaving;
        }

        /// <summary>
        ///Method thats parses the given string into a list of predictions with prediction value und percentage.
        /// </summary>
        /// <param name="toParse">String that is parsed to a list of predictions.</param>
        /// <returns></returns>
        public static List<Prediction> ParseToListOfPredictions(string toParse)
        {
            var predictionLine = toParse.Split(new[] { Environment.NewLine }, StringSplitOptions.RemoveEmptyEntries);
            List<Prediction> predictions = new List<Prediction>();
            foreach (var line in predictionLine)
            {
                Prediction prediction = ParseToPrediction(line);
                predictions.Add(prediction);
            }

            return predictions;
        }

		/// <summary>
		/// Converts a boolean to a string. If the value is true the string will be "An", otherwise it will be "Aus".
		/// </summary>
		/// <param name="isEnabled">Boolean value that represents if a control is enabled.</param>
		/// <returns>The converted string.</returns>
	    public static string ParseToString(bool isEnabled)
	    {
		    return isEnabled ? Properties.Resources.On : Properties.Resources.Off;
	    }

        /// <summary>
        /// Converts a boolean to a string. If the value is true the string will be "number", otherwise it will be "letter".
        /// </summary>
        /// <param name="isEnabled">Boolean value that represents if a control is enabled.</param>
        /// <returns>The converted string.</returns>
        public static string ParseToModelMode(bool isEnabled)
        {
            return isEnabled ? Properties.Resources.ModelNumber : Properties.Resources.ModelLetter;
        }
    }
}
