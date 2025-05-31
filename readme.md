# Stock Oracle MVP - README

## Overview

Stock Oracle is an AI-powered financial analysis platform designed to identify investment opportunities in the "picks and shovels" companies supporting the AI industry's growth. While most investors focus on major AI companies, Stock Oracle targets the overlooked infrastructure providers - smaller companies supplying essential components, materials, and services needed for AI data center expansion.

This MVP implements the core functionality of Stock Oracle, including:

- Multi-dimensional correlation engine for identifying growth patterns
- Supply chain relationship mapping
- News and signals feed with sentiment analysis
- Interactive dashboard with dark/light theme switching
- Company profile analysis with correlation visualization

## Installation

### System Requirements

- Python 3.8 or higher
- macOS (M4 compatible) or Linux
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space

### Installation Steps

1. Clone the repository or extract the ZIP file to your desired location

2. Open Terminal and navigate to the project directory:
   ```
   cd /path/to/stock_oracle_mvp
   ```

3. Run the installation script:
   ```
   chmod +x install.sh
   ./install.sh
   ```

4. The script will:
   - Check for Python and pip
   - Create a virtual environment
   - Install all required dependencies
   - Set up configuration files
   - Provide instructions for running the application

### Running the Application

1. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

2. Start the application:
   ```
   python -m flask run
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Features

### Dashboard

- **Stock Discovery Panel**: View top stock picks based on correlation analysis
- **Multi-Dimensional Correlation Visualizer**: Interactive network graph showing relationships between AI, power, and water infrastructure companies
- **Supply Chain Relationship Map**: Visualize supply chain connections between companies
- **Growth Pattern Matcher**: Compare growth patterns across different sectors
- **News and Signals Feed**: Latest news with sentiment analysis

### Theme Switching

- Toggle between dark and light themes using the switch in the top-right corner
- Theme preference is saved between sessions

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   - If you encounter "ModuleNotFoundError", try reinstalling the specific package:
   ```
   pip install --force-reinstall --no-cache-dir package_name
   ```

2. **Port Already in Use**
   - If port 5000 is already in use, specify a different port:
   ```
   flask run --port=5001
   ```

3. **M4 Mac-Specific Issues**
   - Ensure you're using Python 3.8+ compatible with ARM architecture
   - If you encounter SSL certificate issues, update your certificates:
   ```
   /Applications/Python 3.x/Install Certificates.command
   ```

4. **Application Not Loading**
   - Check if Flask is running in the terminal
   - Try accessing the application at http://127.0.0.1:5000 instead of localhost
   - Restart the application if it becomes unresponsive

## Next Steps

This MVP demonstrates the core functionality of Stock Oracle. Future enhancements will include:

- Advanced machine learning models for more accurate correlation detection
- Expanded data sources and real-time updates
- Enhanced visualization capabilities
- User accounts and customizable watchlists
- Mobile application support

## Feedback

We welcome your feedback on this MVP! Please share your thoughts, suggestions, and any issues you encounter to help us improve the platform.

## License

See the LICENSE file for details.
