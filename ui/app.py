"""
Entry point for the Mental Health Pattern Recognition Assistant GUI.

This module provides a simple entry point to launch the GUI application.
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox

# Add parent directory to path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MentalHealthApp(tk.Tk):
    """
    Main application window for the Mental Health Pattern Recognition Assistant GUI.
    """
    
    def __init__(self, data_dir="../data", output_dir="../visualization"):
        """
        Initialize the main application window.
        
        Args:
            data_dir: Directory for data storage
            output_dir: Directory for visualization output
        """
        super().__init__()
        
        # Set up the main window
        self.title("Mental Health Pattern Recognition Assistant")
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        # Create a welcome label
        welcome_label = tk.Label(
            self, 
            text="Welcome to the Mental Health Pattern Recognition Assistant",
            font=("Arial", 16, "bold")
        )
        welcome_label.pack(pady=50)
        
        description_label = tk.Label(
            self,
            text="This application helps you track your mood and identify patterns and correlations\n"
                 "that can provide insights into factors affecting your mental wellbeing.",
            font=("Arial", 12),
            justify=tk.CENTER
        )
        description_label.pack(pady=20)
        
        # Create a frame for buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=30)
        
        # Add buttons for main actions
        tk.Button(
            button_frame,
            text="Record Mood",
            font=("Arial", 12),
            width=20,
            height=2,
            command=self.record_mood
        ).pack(pady=10)
        
        tk.Button(
            button_frame,
            text="View Data",
            font=("Arial", 12),
            width=20,
            height=2,
            command=self.view_data
        ).pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Run Analysis",
            font=("Arial", 12),
            width=20,
            height=2,
            command=self.run_analysis
        ).pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Generate Visualizations",
            font=("Arial", 12),
            width=20,
            height=2,
            command=self.generate_visualizations
        ).pack(pady=10)
    
    def record_mood(self):
        """Open the mood recording dialog."""
        tk.messagebox.showinfo("Record Mood", "This feature will be implemented in the full version.")
    
    def view_data(self):
        """Open the data viewing dialog."""
        tk.messagebox.showinfo("View Data", "This feature will be implemented in the full version.")
    
    def run_analysis(self):
        """Run the analysis."""
        tk.messagebox.showinfo("Run Analysis", "This feature will be implemented in the full version.")
    
    def generate_visualizations(self):
        """Generate visualizations."""
        tk.messagebox.showinfo("Generate Visualizations", "This feature will be implemented in the full version.")

def main():
    """Main function to run the application."""
    app = MentalHealthApp()
    app.mainloop()

if __name__ == "__main__":
    main()
