using System;
using System.Collections.Generic;
using Traicy.GUI.Data;

namespace Traicy.GUI.Logic
{
    public class PythonOutputParser
    {
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
        public static IEnumerable<Prediction> ParseToListOfPredictions(string toParse)
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
