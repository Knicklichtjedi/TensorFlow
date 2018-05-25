using System;
using System.Collections.Generic;
using Traicy.GUI.Data;

namespace Traicy.GUI.Logic
{
    public class PythonOutputParser
    {
        public static List<string> ParseStringToList(string toParse)
        {
            var parsedLoadingString = Parse(toParse);
            List<string> possibleFileExtensionsForImages = new List<string>();
            for (int i = 0; i < parsedLoadingString.Length; i++)
            {
                possibleFileExtensionsForImages.Add(parsedLoadingString[i]);
            }

            return possibleFileExtensionsForImages;
        }

        public static string ParseListToString(List<string> toParse)
        {
            string concatenatedFileExtensionStringForJsonSettingsSaving = string.Empty;
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

        private static string[] Parse(string toParse)
        {
            var parsedStrings = toParse.Split(new[] {","}, StringSplitOptions.RemoveEmptyEntries);
            return parsedStrings;
        }

        public static Prediction ParseToPrediction(string toParse)
        {
            var parsedLine = Parse(toParse);
            Prediction prediction = new Prediction
            {
                PredictedValue = parsedLine[0],
                PredictionPercentage = parsedLine[1]
            };

            return prediction;
        }

        /// <summary>
        ///Method thats parses the given parse string into a list of predictions with prediction value und percentage.
        /// </summary>
        /// <param name="toParse"></param>
        /// <returns></returns>
        public static List<Prediction> ParseToListOfPredictions(string toParse)
        {
            //TODO: überprüfen, ob das so mit newline funktioniert
            var predictionLine = toParse.Split(new[] { Environment.NewLine }, StringSplitOptions.RemoveEmptyEntries);
            List<Prediction> predictions = new List<Prediction>();
            foreach (var line in predictionLine)
            {
                Prediction prediction = ParseToPrediction(line);
                predictions.Add(prediction);
            }

            return predictions;
        }
    }
}
