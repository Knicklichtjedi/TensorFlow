using System.Collections.Generic;
using System.Linq;
using System.Speech.Synthesis;

namespace Traicy.GUI.Logic
{
    public class TextToSpeech
    {
        private static SpeechSynthesizer _speaker;

        public TextToSpeech()
        {
            _speaker = new SpeechSynthesizer();
        }

        //zusätzliche Methode, kann manchmal nützlich sein
        private static List<VoiceInfo> GetInstalledVoices()
        {
            var listOfVoiceInfo = from voice
                    in _speaker.GetInstalledVoices()
                select voice.VoiceInfo;

            return listOfVoiceInfo.ToList<VoiceInfo>();
        }

        public void InvokeAsyncTextToSpeech(string text)
        {
            //get all available voices
            var voices = GetInstalledVoices();
            if (voices?.Count > 0)
            {
                string voiceName = string.Empty;

                var voice = voices.FirstOrDefault(x => x.Culture.Name == "de-DE");
                if (voice != null)
                {
                    voiceName = voice.Name;
                }

                _speaker.SetOutputToDefaultAudioDevice();
                //Geschwindigkeit (-10 - 10)
                _speaker.Rate = -2;
                //Lautstärke (0-100)
                _speaker.Volume = 100;
                _speaker.SelectVoice(voiceName); //englische Version
                //_speaker.SelectVoice("Microsoft Zira Desktop"); //englische Version
                //_speaker.SelectVoice("Microsoft Anna"); //englische Version

                //Such passende Stimme zu angegebenen Argumenten
                //_speaker.SelectVoiceByHints(VoiceGender.Female, VoiceAge.Teen);
                //Text wird ausgegeben (abbrechen mit speaker.CancelAsync())

                _speaker.SpeakAsync(text);
            }
        }
    }
}
