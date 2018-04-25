using Traicy.GUI.Contracts;

namespace Traicy.GUI.Logic
{
    public class EventHandling
    {
        //public delegate void TextToSpeechChangedEventHandler(bool isEnabled);
        //public delegate void FilteredImagesChangedEventHandler(bool isEnabled);
        //public delegate void PythonInterpreterChangedEventHandler(string pythonInterpreterPath);
        public delegate void SettingsChangedEventHandler(ISettingProperties settings);

        //public static event TextToSpeechChangedEventHandler TextToSpeechEvent;
        //public static event FilteredImagesChangedEventHandler FilteredImagesEvent;
        //public static event PythonInterpreterChangedEventHandler PythonInterpreterChangedEvent;
        public static event SettingsChangedEventHandler SettingsChangedEvent;


        //public static void OnTextToSpeechEvent(bool isEnabled)
        //{
        //    TextToSpeechEvent?.Invoke(isEnabled);
        //}

        //public static void OnFilteredImagesEvent(bool isEnabled)
        //{
        //    FilteredImagesEvent?.Invoke(isEnabled);
        //}

        //public static void OnPythonInterpreterChangedEvent(string pythonInterpreterPath)
        //{
        //    PythonInterpreterChangedEvent?.Invoke(pythonInterpreterPath);
        //}

        public static void OnSettingsChangedEvent(ISettingProperties settings)
        {
            SettingsChangedEvent?.Invoke(settings);
        }
    }
}
