using IronPython.Hosting;

namespace Traicy.GUI.Logic
{
    public class IronPythonConnection
    {
        public void InitializeIronPython()
        {
            //TODO: extra als zweite Variante?
            //var engine = Python.CreateEngine(); // Extract Python language engine from their grasp
            //var scope = engine.CreateScope(); // Introduce Python namespace (scope)
            //                                  //var d = new Dictionary<string, object>
            //                                  //{
            //                                  //    { "serviceid", serviceid},
            //                                  //    { "parameter", parameter}
            //                                  //}; // Add some sample parameters. Notice that there is no need in specifically setting the object type, interpreter will do that part for us in the script properly with high probability

            //ScriptSource source = engine.CreateScriptSourceFromFile("ImageFilter.py");

            //source.Execute(scope);
            //var t = engine.Operations.Invoke("test");
            //scope.SetVariable("params", d); // This will be the name of the dictionary in python script, initialized with previously created .NET Dictionary
            //ScriptSource source = engine.CreateScriptSourceFromFile("PATH_TO_PYTHON_SCRIPT_FILE"); // Load the script
            //object result = source.Execute(scope);
            //parameter = scope.GetVariable<string>("parameter"); // To get the finally set variable 'parameter' from the python script;

            //using IronPython

        }

        public string GetPrediction()
        {
            //TODO: auslagern
            var ironPythonRuntime = Python.CreateRuntime();
            //string directory = System.IO.Directory.GetParent(Environment.CurrentDirectory).ToString();
            dynamic loadIPython = ironPythonRuntime.UseFile("ImageFilter.py"); //@"C:\Users\Eva\Documents\GitHub\TensorFlow\traicy\gui\Traicy.GUI\resources\ImageFilter.py"
            var prediction = loadIPython.test();

            return string.IsNullOrEmpty(prediction) ? "prediction" : prediction;
        }
    }
}
