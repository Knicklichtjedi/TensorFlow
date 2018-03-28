using System;
using System.Windows;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;

namespace Traicy.GUI.View
{
    /// <summary>
    /// Interaktionslogik für MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();

            //using IronPython
            ScriptRuntime ironPythonRuntime = Python.CreateRuntime();
            //string directory = System.IO.Directory.GetParent(Environment.CurrentDirectory).ToString();
            //dynamic loadIPython = ironPythonRuntime.UseFile(@"../filters/ImageFilter.py");
            //loadIPython.MethodCall("main");

        }
    }
}
