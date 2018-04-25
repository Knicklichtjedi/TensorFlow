using System.Windows;
using Traicy.GUI.Data;
using Traicy.GUI.Logic;

namespace Traicy.GUI.View
{
    /// <summary>
    /// Interaktionslogik für FilteredImagesWindow.xaml
    /// </summary>
    public partial class FilteredImagesWindow : Window
    {
        public FilteredImagesWindow()
        {
            InitializeComponent();

            LoadFilteredImages();
        }

        private void LoadFilteredImages()
        {
            FilteredImages filteredImages = new WebcamHelper().GetFilteredImages();

            if (filteredImages != null)
            {
                BinaryImage.Source = filteredImages.BinaryImage;
                SkeletonImage.Source = filteredImages.SkeletonImage;
            }
        }
    }
}
