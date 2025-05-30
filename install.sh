#!/bin/bash
# install.sh - Installation script for Stock Oracle MVP

# Set up colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}"
echo "  ____  _             _      ___                 _      "
echo " / ___|| |_ ___   ___| | __ / _ \ _ __ __ _  ___| | ___ "
echo " \___ \| __/ _ \ / __| |/ // | | | '__/ _\` |/ __| |/ _ \\"
echo "  ___) | || (_) | (__|   <| |_| | | | (_| | (__| |  __/"
echo " |____/ \__\___/ \___|_|\_\\\\___/|_|  \__,_|\___|_|\___|"
echo -e "${NC}"
echo -e "${YELLOW}Installation Script${NC}"
echo

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to display GUI for missing dependencies
display_gui() {
    if command_exists zenity; then
        zenity --question --title="Stock Oracle Installation" --text="The following dependencies are missing:\n$1\n\nWould you like to install them automatically?" --width=400
        return $?
    elif command_exists whiptail; then
        whiptail --title "Stock Oracle Installation" --yesno "The following dependencies are missing:\n$1\n\nWould you like to install them automatically?" 15 60
        return $?
    else
        echo -e "${YELLOW}The following dependencies are missing:${NC}"
        echo "$1"
        read -p "Would you like to install them automatically? (y/n) " -n 1 -r
        echo
        [[ $REPLY =~ ^[Yy]$ ]]
        return $?
    fi
}

# Check for Python 3.8+
echo -e "${BLUE}Checking Python version...${NC}"
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
        echo -e "${GREEN}Python $PYTHON_VERSION detected. ✓${NC}"
        PYTHON_CMD="python3"
    else
        echo -e "${RED}Python 3.8+ is required, but $PYTHON_VERSION was found.${NC}"
        exit 1
    fi
else
    echo -e "${RED}Python 3 not found. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Check for pip
echo -e "${BLUE}Checking pip installation...${NC}"
if command_exists pip3; then
    echo -e "${GREEN}pip3 detected. ✓${NC}"
    PIP_CMD="pip3"
elif command_exists pip; then
    echo -e "${GREEN}pip detected. ✓${NC}"
    PIP_CMD="pip"
else
    echo -e "${RED}pip not found. Please install pip.${NC}"
    exit 1
fi

# Create virtual environment
echo -e "${BLUE}Setting up virtual environment...${NC}"
VENV_DIR="venv"

if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Using existing environment.${NC}"
else
    echo -e "${BLUE}Creating new virtual environment...${NC}"
    $PYTHON_CMD -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create virtual environment.${NC}"
        echo -e "${YELLOW}Attempting to install venv module...${NC}"
        $PIP_CMD install --user virtualenv
        $PYTHON_CMD -m venv $VENV_DIR
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to create virtual environment. Please install the venv module manually.${NC}"
            exit 1
        fi
    fi
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    source $VENV_DIR/bin/activate
else
    # Linux/Unix
    source $VENV_DIR/bin/activate
fi

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
echo -e "${YELLOW}This may take a few minutes...${NC}"
pip install --force-reinstall --no-cache-dir -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install some dependencies.${NC}"
    echo -e "${YELLOW}Attempting to install dependencies individually...${NC}"
    
    # List of core dependencies
    DEPENDENCIES=(
        "flask"
        "pandas"
        "numpy"
        "plotly"
        "dash"
        "dash-bootstrap-components"
        "python-dotenv"
        "yfinance"
        "networkx"
    )
    
    MISSING=""
    for dep in "${DEPENDENCIES[@]}"; do
        pip install --force-reinstall --no-cache-dir $dep
        if [ $? -ne 0 ]; then
            MISSING="$MISSING\n- $dep"
        fi
    done
    
    if [ ! -z "$MISSING" ]; then
        display_gui "$MISSING"
        if [ $? -eq 0 ]; then
            echo -e "${BLUE}Installing missing dependencies with sudo...${NC}"
            for dep in "${DEPENDENCIES[@]}"; do
                pip install --force-reinstall --no-cache-dir $dep
            done
        else
            echo -e "${RED}Some dependencies could not be installed. The application may not function correctly.${NC}"
        fi
    fi
else
    echo -e "${GREEN}All dependencies installed successfully. ✓${NC}"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    echo "FLASK_APP=app.py" > .env
    echo "FLASK_ENV=development" >> .env
    echo "DEBUG=True" >> .env
    echo -e "${GREEN}.env file created. ✓${NC}"
fi

# Set up database directory
echo -e "${BLUE}Setting up data directory...${NC}"
mkdir -p data
echo -e "${GREEN}Data directory created. ✓${NC}"

# Installation complete
echo
echo -e "${GREEN}Stock Oracle MVP installation complete!${NC}"
echo
echo -e "${BLUE}To run the application:${NC}"
echo -e "  1. Activate the virtual environment:"
echo -e "     ${YELLOW}source venv/bin/activate${NC}"
echo -e "  2. Start the application:"
echo -e "     ${YELLOW}python -m flask run${NC}"
echo
echo -e "${BLUE}To access the dashboard:${NC}"
echo -e "  Open your browser and navigate to: ${YELLOW}http://localhost:5000${NC}"
echo
echo -e "${BLUE}For more information, see the README.md file.${NC}"
echo

# Exit with success
exit 0
