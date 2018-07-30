using System;
using System.IO;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
using System.Windows;
using System.Windows.Interop;
using System.Windows.Media;
using System.Windows.Media.Imaging;

namespace Traicy.GUI.Logic
{
    /// <summary>
    /// Provides methods for using the webcam and converting media.
    /// </summary>
    public class WebcamHelper
    {
        [DllImport("gdi32.dll", EntryPoint = "DeleteObject")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool DeleteObject([In] IntPtr hObject);

        /// <summary>
        /// Parses given webcam bitmap to ImageSource.
        /// </summary>
        /// <param name="bmp">The given image as bitmap.</param>
        /// <returns>ImageSource as type that is used in the view.</returns>
        public static ImageSource ImageSourceForBitmap(Bitmap bmp)
        {
            var handle = bmp.GetHbitmap();
            try
            {
                return Imaging.CreateBitmapSourceFromHBitmap(handle, IntPtr.Zero, Int32Rect.Empty, BitmapSizeOptions.FromEmptyOptions());
            }
            finally { DeleteObject(handle); }
        }

		/// <summary>
		/// Takes a picture of the given webcam frame and saves it with current timestamp to the images folder. The filepath of the saved image is returned for further processing.
		/// </summary>
		/// <param name="picture">Webcam frame that is saved as bitmap.</param>
		/// <returns>Absolute filepath of the saved image.</returns>
		public static string TakePicture(Bitmap picture)
        {
            string filename = $"{DateTime.Now:dd_MM_yy hh_mm_ss}.{Properties.Resources.ImageTypePNG}";
            if (!Directory.Exists(Properties.Resources.ImageFolderPath))
            {
                Directory.CreateDirectory(Properties.Resources.ImageFolderPath);
            }
            string filePath = $"{Properties.Resources.ImageFolderPath}\\{filename}";
            picture.Save(filePath, ImageFormat.Png);
            string absolutePath = Path.GetFullPath(filePath);
            return absolutePath;
        }

		/// <summary>
		/// Returns bitmap from the given image source.
		/// </summary>
		/// <param name="source">Image source (Uri) as string.</param>
		/// <returns>Bitmap from the image that is read from source.</returns>
        public static Bitmap GetBitmapImageFromSource(string source)
        {
            Image image = Image.FromFile(source);
            Bitmap bitmap = new Bitmap(image);
            return bitmap;
        }
    }
}
