using System.Collections.Generic;
using Traicy.GUI.Contracts;

namespace Traicy.GUI.Data
{
    public class LoadingSettings : ILoadingSettings
    {
        [Newtonsoft.Json.JsonProperty(PropertyName = "possible_filename")]
        public List<string> PossibleImageFileTypes { get; set; }
    }
}
