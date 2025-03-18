"""
Test script for the Mental Health Pattern Recognition Assistant GUI.

This script tests the basic functionality of the GUI application.
"""

import os
import sys
import unittest
from unittest.mock import patch

# Add parent directory to path to import from src and ui
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the GUI application
from ui.app import MentalHealthApp

class TestGUI(unittest.TestCase):
    """Test cases for the GUI application."""
    
    @patch('tkinter.Tk.mainloop')
    def test_app_initialization(self, mock_mainloop):
        """Test that the application initializes correctly."""
        app = MentalHealthApp()
        
        # Check that the window title is set correctly
        self.assertEqual(app.title(), "Mental Health Pattern Recognition Assistant")
        
        # Check that the window size is set
        # Note: The actual geometry string may vary by platform, so we just check that it's not empty
        self.assertNotEqual(app.geometry(), "")
        
        # Check that the minimum window size is set correctly
        self.assertEqual(app.minsize(), (800, 600))
        
        # Clean up
        app.destroy()
    
    @patch('tkinter.messagebox.showinfo')
    def test_button_callbacks(self, mock_showinfo):
        """Test that the button callbacks work correctly."""
        app = MentalHealthApp()
        
        # Test the record_mood callback
        app.record_mood()
        mock_showinfo.assert_called_with("Record Mood", "This feature will be implemented in the full version.")
        
        # Test the view_data callback
        app.view_data()
        mock_showinfo.assert_called_with("View Data", "This feature will be implemented in the full version.")
        
        # Test the run_analysis callback
        app.run_analysis()
        mock_showinfo.assert_called_with("Run Analysis", "This feature will be implemented in the full version.")
        
        # Test the generate_visualizations callback
        app.generate_visualizations()
        mock_showinfo.assert_called_with("Generate Visualizations", "This feature will be implemented in the full version.")
        
        # Clean up
        app.destroy()

if __name__ == '__main__':
    unittest.main()
