namespace Traicy.GUI.Contracts
{
    public interface IGuiSettings
    {
        bool TextToSpeechIsEnabled { get; set; }
        bool ShowFilteredImagesIsEnabled { get; set; }
        string PythonInterpreterPath { get; set; }
        //TODO: weitere GUI settings?
    }
}
