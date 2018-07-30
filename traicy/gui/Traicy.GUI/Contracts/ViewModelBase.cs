using System.ComponentModel;

namespace Traicy.GUI.Contracts
{
	/// <summary>
	/// Base class that implements the INotifyPropertyChanged interface and is responsible for handling changes of properties in the view.
	/// </summary>
	public class ViewModelBase : INotifyPropertyChanged
	{
		public event PropertyChangedEventHandler PropertyChanged;

		/// <summary>
		/// Invokes the PropertyChangedEvent for the property with the propertyName.
		/// </summary>
		/// <param name="propertyName">Defines which property has changed.</param>
		protected virtual void OnPropertyChanged(string propertyName)
		{
			var handler = PropertyChanged;
			handler?.Invoke(this, new PropertyChangedEventArgs(propertyName));
		}
	}
}
