# Mental Health Pattern Recognition Assistant - GUI

This directory contains the graphical user interface (GUI) for the Mental Health Pattern Recognition Assistant.

## Overview

The GUI provides a user-friendly interface for interacting with the Mental Health Pattern Recognition Assistant. It allows users to:

- Record mood, activities, sleep, and medication data
- View recorded data in a structured format
- Run pattern recognition and correlation analyses
- Generate visualizations of data and analysis results
- View personalized insights based on the analyses

## Running the Application

To run the GUI application, navigate to the `ui` directory and run:

```bash
python app.py
```

## Current Implementation Status

The current implementation is a basic prototype that demonstrates the UI layout and navigation. The following features are implemented:

- Basic application window with welcome screen
- Main navigation buttons for key features
- Placeholder dialogs for main functionality

## Future Enhancements

The following enhancements are planned for future versions:

- Complete implementation of data entry forms
- Data visualization displays
- Analysis results presentation
- Settings configuration
- Dashboard with key statistics and insights
- Export and import functionality

## Dependencies

The GUI requires the following dependencies:

- Python 3.6 or higher
- Tkinter (included with most Python installations)
- Matplotlib (for visualizations)
- The core Mental Health Pattern Recognition Assistant modules

## Architecture

The GUI follows a modular architecture:

- `app.py`: Main entry point for the application
- Future modules will include:
  - Data entry forms
  - Data visualization components
  - Analysis results displays
  - Settings panels
