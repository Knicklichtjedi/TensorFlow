using System;

namespace Traicy.GUI.Logic
{
    public class PythonOutputParser
    {
        public static string[] Parse(string toParse)
        {
            var parsedStrings = toParse.Split(new[] {","}, StringSplitOptions.RemoveEmptyEntries);
            return parsedStrings;
        }
    }
}
