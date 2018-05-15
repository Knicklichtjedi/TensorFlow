using System;
using System.IO;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;
using System.Runtime.InteropServices;
using System.Windows;
using System.Windows.Interop;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using Traicy.GUI.Data;

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
        /// Parses given webcam bitmap to ImageSource 
        /// </summary>
        /// <param name="bmp"></param>
        /// <returns></returns>
        public ImageSource ImageSourceForBitmap(Bitmap bmp)
        {
            var handle = bmp.GetHbitmap();
            try
            {
                return Imaging.CreateBitmapSourceFromHBitmap(handle, IntPtr.Zero, Int32Rect.Empty, BitmapSizeOptions.FromEmptyOptions());
            }
            finally { DeleteObject(handle); }
        }

        public string TakePicture(Bitmap picture)
        {
            string filename = $"{DateTime.Now:dd_MM_yy hh_mm_ss}.png";
            if (!Directory.Exists("images"))
            {
                Directory.CreateDirectory("images");
            }
            string filePath = $"images\\{filename}";
            picture.Save(filePath, ImageFormat.Png);
            string absolutePath = Path.GetFullPath(filePath);
            return absolutePath;
        }

        internal FilteredImages GetFilteredImages()
        {
            FilteredImages filteredImages = null;

            var filePath = @"filtered\";
            var directory = new DirectoryInfo(filePath);
            //var directoryInfo = directory.GetDirectories().OrderByDescending(d => d.LastWriteTime).First();
            //filePath = $"{filePath}{directoryInfo}\\filtered.png_borders.png";
            //filePath =
            //    @"C:\Users\Eva\Documents\GitHub\TensorFlow\traicy\gui\Traicy.GUI\bin\Debug\filtered\2018_04_25_x_02_29_49\test.png";

            try
            {
                //TODO: 
                filteredImages = new FilteredImages
                {
                    //BinaryImage = GetBitmapImageFromSource(filePath),
                    BinaryImage = ImageSourceForBitmap(GetBitmapImageFromSource($"{filePath}\\filtered.png_borders.png")),
                    SkeletonImage = ImageSourceForBitmap(GetBitmapImageFromSource($"{filePath}\\filtered.png_centered.png"))
                };
            }
            catch (Exception e)
            {
                Logger.Log(e.Message);
            }

            return filteredImages;
        }

        public static Bitmap GetBitmapImageFromSource(string source)
        {
            Image image = Image.FromFile(source);
            Bitmap bitmap = new Bitmap(image);
            return bitmap;
        }
    }
}
