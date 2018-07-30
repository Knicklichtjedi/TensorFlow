using System;
using System.IO;
using System.Text;

namespace Traicy.GUI.Logic
{
	/// <summary>
	/// Class that provides functionality for logging errors and warnings (exception handling) that occur in the process.
	/// </summary>
	public class Logger
    {
        /// <summary>
        /// Writes the given message to a logfile and adds current date and time for better evaluation.
        /// </summary>
        /// <param name="logMessage">Message that is logged in the logfile.</param>
        public static void Log(string logMessage)
        {
            StringBuilder stringBuilder = new StringBuilder();
            stringBuilder.Append($"{DateTime.Now.ToLongTimeString()} {DateTime.Now.ToLongDateString()}: {logMessage}{Environment.NewLine}");
            File.AppendAllText(Properties.Resources.Logfile, stringBuilder.ToString());
        }
    }
}