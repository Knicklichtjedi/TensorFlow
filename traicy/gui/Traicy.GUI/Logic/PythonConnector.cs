﻿using System;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Text;
using IronPython.Hosting;

namespace Traicy.GUI.Logic
{
    public class PythonConnector
    {

        public string PythonInterpreterPath { get; set; }

        public PythonConnector()
        {
            //EventHandling.PythonInterpreterChangedEvent += OnPythonInterpreterChanged;
        }

        private void OnPythonInterpreterChanged(string pythoninterpreterpath)
        {
            PythonInterpreterPath = pythoninterpreterpath;
        }

        [Obsolete("IronPython isn't compatible with version 3.6 of Python and can't be used with TensorFlow either.")]
        public void ExecutePythonScript()
        {
            try
            {
                var engine = Python.CreateEngine(); 
                var paths = engine.GetSearchPaths();
                //add packages to import all needed modules for IronPython
                paths.Add(@"C:\Users\Eva\Anaconda3\envs\customTFLearn\Lib"); //add python script files to the ironPython paths
                paths.Add(@"C:\Users\Eva\Anaconda3\envs\customTFLearn\Lib\site-packages"); //add all side packages and modules e.g. numpy, skimage to ironPython paths
                engine.SetSearchPaths(paths);
                var scope = engine.CreateScope();

                var source = engine.CreateScriptSourceFromFile(@"../Debug/filters/Test.py");
                source.Execute();
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
            
        }

        [Obsolete("IronPython isn't compatible with version 3.6 of Python and can't be used with TensorFlow either.")]
        public void ExecutePythonScript2()
        {
            var ironPythonRuntime = Python.CreateRuntime();
            //string directory = System.IO.Directory.GetParent(Environment.CurrentDirectory).ToString();
            dynamic loadIPython = ironPythonRuntime.UseFile(@"../filters/Test.py");
            var prediction = loadIPython.test(); //call specific function
        }

        public string GetPrediction(string absoluteImagePath)
        {
            //TODO: als Ressourcen-String verwenden
            //string pythonScriptFilePath = @"C:\Users\Eva\Documents\GitHub\TensorFlow\traicy\gui\Traicy.GUI\bin\Debug\filters\Test2.py";
            string pythonScriptFilePath = @"python_resources\predict_number.py"; //TODO: importierte Python-Module werden nicht erkannt
            
            var result = StartPythonProcess(pythonScriptFilePath, absoluteImagePath);
            if (!string.IsNullOrEmpty(result))
            {
                var parsedPrediction = PythonOutputParser.ParseToListOfPredictions(result);
                string prediction = string.Empty;
                //TODO: Sprachausgabe bei mehreren Predictions so lassen?

                StringBuilder stringBuilder = new StringBuilder();
                stringBuilder.Append(prediction);


                string numberOfChunksFound = parsedPrediction.Count.ToString();

                if (parsedPrediction.Count == 1)
                {
                    //string outputChunks = "I found the number ";
                    string outputChunks = "Die gefundene Nummer ist ";
                    stringBuilder.Append(outputChunks);
                    var number = parsedPrediction[0].PredictedValue;
                    stringBuilder.Append(number);
                    stringBuilder.Append(", ");

                }
                else if (parsedPrediction.Count >= 2)
                {
                    //string outputChunks = $"I found the following {numberOfChunksFound} numbers: ";
                    stringBuilder.Append("Ich habe die folgenden ");
                    stringBuilder.Append(numberOfChunksFound);
                    stringBuilder.Append(" Zahlen gefunden: ");
                
                    //stringBuilder.Append(outputChunks);
                    foreach (var pred in parsedPrediction)
                    {
                        var number = pred.PredictedValue;
                        var probability = pred.PredictionPercentage; //OBSOLETE bis NN überarbeitet wurde
                                                                     //prediction += $"The number is {letter} with a probability of {probability}"; //OBSOLETE

                        stringBuilder.Append(number);
                        stringBuilder.Append(", ");
                        //prediction += $"The number is {letter}";
                    }
                }
                //stringBuilder.Append("That's all.");
                stringBuilder.Append("Mehr kann ich nicht erkennen.");
                return stringBuilder.ToString();
            }
            //return "There has been an error!";
            return "Es ist ein Fehler aufgetreten!";
        }

        //TODO: settings als parameter übergeben?
        private string StartPythonProcess(string command, string args)
        {
            ProcessStartInfo start = new ProcessStartInfo
            {
                FileName = PythonInterpreterPath, //custom path from settings file
                //FileName = @"C:\Users\Eva\Anaconda3\envs\customEnv\python.exe", //eva laptop            
                //FileName = @"C:\Users\katha\AppData\Local\Programs\Python\Python36\python.exe", //katl
                Arguments = $"\"{command}\" \"{args}\"",
                UseShellExecute = false, // don't use windows cmd
                CreateNoWindow = true,
                RedirectStandardOutput = true, // Any output, generated by application will be redirected back
                RedirectStandardError = true // Any error in standard output will be redirected back (for example exceptions)
            };

            //var test = start.WorkingDirectory;
            try
            {
                using (Process process = Process.Start(start))
                {
                    if (process != null)
                    {
                        process.WaitForExit();
                        using (StreamReader reader = process.StandardOutput)
                        {
                            string stderr =
                                process.StandardError.ReadToEnd(); // Here are the exceptions from our Python script
                            Logger.Log(stderr);
                            string
                                result = reader.ReadToEnd(); // Here is the result of StdOut(for example: print "test")
                            return result;
                        }
                    }
                }
            }
            catch (Win32Exception e)
            {
                Logger.Log(e.Message);
            }
            catch (Exception e)
            {
                Logger.Log(e.Message);
            }

            return string.Empty;
        }
    }
}
