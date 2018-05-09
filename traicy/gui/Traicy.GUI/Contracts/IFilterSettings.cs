namespace Traicy.GUI.Contracts
{
    public interface IFilterSettings
    {
        float Canny { get; set; }
        float BinaryGauss { get; set; }
        float BinaryThreshold { get; set; }
        int GreenLow { get; set; }
        int GreenHigh { get; set; }
        float GreenSaturation { get; set; }
        float GreenBrightness { get; set; }
        float Schmiering { get; set; }
        float MinimalOutlineSizeChunking { get; set; }

    }
}
