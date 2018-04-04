using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;
using System.Speech.Synthesis;

namespace Traicy.GUI.View
{
    /// <summary>
    /// Interaktionslogik für MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private static SpeechSynthesizer _speaker;

        public MainWindow()
        {
            InitializeComponent();

            //using IronPython
            ScriptRuntime ironPythonRuntime = Python.CreateRuntime();
            //string directory = System.IO.Directory.GetParent(Environment.CurrentDirectory).ToString();
            //dynamic loadIPython = ironPythonRuntime.UseFile(@"../filters/ImageFilter.py");
            //loadIPython.MethodCall("main");

        }

        private void ButtonSettings_OnClick(object sender, RoutedEventArgs e)
        {
            new SettingsWindow().ShowDialog();


        }

        //zusätzliche Methode, kann manchmal nützlich sein
        private static List<VoiceInfo> GetInstalledVoices()
        {
            var listOfVoiceInfo = from voice
                    in _speaker.GetInstalledVoices()
                select voice.VoiceInfo;

            return listOfVoiceInfo.ToList<VoiceInfo>();
        }

        private void ButtonStartObjectDetection_OnClick(object sender, RoutedEventArgs e)
        {
            TextToSpeechTest();
        }

        private static void TextToSpeechTest()
        {
            _speaker = new SpeechSynthesizer();

            //
            var voices = GetInstalledVoices();

            //In dem Fall unnötig, aber falls zB vorher OutputToWav eingestellt war
            _speaker.SetOutputToDefaultAudioDevice();
            //Geschwindigkeit (-10 - 10)
            _speaker.Rate = 1;
            //Lautstärke (0-100)
            _speaker.Volume = 100;
            _speaker.SelectVoice("Microsoft Zira Desktop");
            //Such passende Stimme zu angegebenen Argumenten
            //_speaker.SelectVoiceByHints(VoiceGender.Female, VoiceAge.Teen);
            //Text wird ausgegeben (abbrechen mit speaker.CancelAsync())
            //_speaker.SpeakAsync("a ist der Buchstabe!");
            _speaker.SpeakAsync("I see an T!");
            _speaker.SpeakAsync("I see an R!");
            _speaker.SpeakAsync("I see an A!");
            _speaker.SpeakAsync("I see an I!");
            _speaker.SpeakAsync("I see an C!");
            _speaker.SpeakAsync("I see an Y!");
            _speaker.SpeakAsync("T R A I C Y");
            _speaker.SpeakAsync("TRAICY");
        }
    }
}
