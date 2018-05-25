﻿using Traicy.GUI.Data;

namespace Traicy.GUI.Contracts
{
    public interface ISettingProperties
    {
        ImageSettings ImageSettings { get; set; }
        FilterSettings FilterSettings { get; set; }
        GuiSettings GuiSettings { get; set; }
        LoadingSettings LoadingSettings { get; set; }
    }
}
