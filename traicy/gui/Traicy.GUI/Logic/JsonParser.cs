using System;
using System.IO;
using Newtonsoft.Json;

namespace Traicy.GUI.Logic
{
    /// <summary>
    /// Class for parsing generic details for shortcuts and programinformation
    /// </summary>
    public class JsonParser
    {
        /// <summary>
        /// Method that generically serializes list of objects into JSON by using the given filepath.
        /// </summary>
        /// <typeparam name="T">Generic type for serialization</typeparam>
        /// <param name="listOfInformation">Generic (list of) objects </param>
        /// <param name="filePath">File destination of the JSON-File</param>
        public static void SerializeToJson<T>(T listOfInformation, string filePath)
        {
            try
            {
                string jsonString = JsonConvert.SerializeObject(listOfInformation, Formatting.Indented);
                File.WriteAllText(filePath, jsonString);
            }
            catch (IOException e)
            {
                Console.WriteLine(e.Message);
            }
        }

        /// <summary>
        /// Method that generically deserializes list of objects from JSON by using the given filepath.
        /// </summary>
        /// <typeparam name="T">Generic type for deserialization</typeparam>
        /// <param name="filePath">File destination of the JSON-File</param>
        /// <returns>Returns generic object that has been deserialized</returns>
        public static T DeserializeFromJson<T>(string filePath)
        {
            T listOfInformation = default(T);

            try
            {
                string jsonString = File.ReadAllText(filePath);
                listOfInformation = JsonConvert.DeserializeObject<T>(jsonString);
            }
            catch (IOException e)
            {
                Console.WriteLine(e.Message);
            }

            return listOfInformation;
        }
    }
}
