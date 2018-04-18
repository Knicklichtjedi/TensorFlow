namespace Traicy.GUI.Logic
{
    public class EventHandling
    {
        public delegate void TextToSpeechChangedEventHandler(bool isEnabled);

        public static event TextToSpeechChangedEventHandler TextToSpeechEvent;


        public static void OnTextToSpeechEvent(bool isenabled)
        {
            TextToSpeechEvent?.Invoke(isenabled);
        }
    }
}
