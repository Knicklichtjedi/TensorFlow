using System.Collections.Generic;
using System.Linq;
using System.Speech.Synthesis;

namespace Traicy.GUI.Logic
{
	/// <summary>
	/// Class that is responsible for handling the Text-To-Speech functionality.
	/// </summary>
    public class TextToSpeech
    {
        private static SpeechSynthesizer _speaker;

        public TextToSpeech()
        {
            _speaker = new SpeechSynthesizer();
        }

		/// <summary>
		/// Returns all installed voices for the operating system (Windows) as List.
		/// </summary>
		/// <returns>List of VoiceInfo objects that can be used to configure the Text-To-Speech output.</returns>
        private static List<VoiceInfo> GetInstalledVoices()
        {
            var listOfVoiceInfo = from voice
                    in _speaker.GetInstalledVoices()
                select voice.VoiceInfo;

            return listOfVoiceInfo.ToList<VoiceInfo>();
        }

		/// <summary>
		/// Invokes the Text-To-Speech algorithm and uses the given text.
		///	Based on the installed voices the first german voice is chosen and used to speak.
		/// </summary>
		/// <param name="text">The given text the speechsynthesizer processes.</param>
        public void InvokeAsyncTextToSpeech(string text)
        {
            //get all available voices
            var voices = GetInstalledVoices();
            if (voices?.Count > 0)
            {
				//use first german voice that is found
                var voice = voices.FirstOrDefault(x => x.Culture.Name == Properties.Resources.GermanVoice);
                if (voice != null)
                {
	                _speaker.SetOutputToDefaultAudioDevice();
	                _speaker.Rate = -2; //speed
	                _speaker.Volume = 100; //max volume
	                _speaker.SelectVoice(voice.Name);
	                _speaker.SpeakAsync(text); //speak
				}
            }
        }
    }
}
