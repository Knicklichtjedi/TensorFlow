using System;
using System.Windows.Input;

namespace Traicy.GUI.Commands
{
	/// <summary>
	/// Class that implements the ICommand interface and is used for defining Commands that are used in the view. 
	/// </summary>
	public class DelegateCommand : ICommand
	{
		private readonly Action<object> _action;

		public event EventHandler CanExecuteChanged;

		public DelegateCommand(Action<object> action)
		{
			_action = action;
			//_canExecute = canExecute;
		}

		public void Execute(object parameter)
		{
			_action(parameter);
		}

		public bool CanExecute(object parameter)
		{
			return true;
		}
	}
}
