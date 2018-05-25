using System.Collections.Generic;

namespace Traicy.GUI.Contracts
{
    public interface ILoadingSettings
    {
        List<string> PossibleImageFileTypes { get; set; }
    }
}