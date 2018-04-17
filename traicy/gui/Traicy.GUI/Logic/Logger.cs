using System;
using System.IO;
using System.Text;

namespace Traicy.GUI.Logic
{
    public class Logger
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="logMessage"></param>
        public static void Log(string logMessage)
        {
            StringBuilder stringBuilder = new StringBuilder();
            stringBuilder.Append($"{DateTime.Now.ToLongTimeString()} {DateTime.Now.ToLongDateString()}: {logMessage}{Environment.NewLine}");
            File.AppendAllText("log.txt", stringBuilder.ToString());
        }
    }
}