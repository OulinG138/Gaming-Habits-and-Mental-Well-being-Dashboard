#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "🚀 Starting project setup..."

# 1. Check if Python is installed
if ! command_exists python3; then
    echo "❌ Python3 is not installed."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "🔄 Installing Python3 on macOS..."
        if ! command_exists brew; then
            echo "🔄 Homebrew is not installed. Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python
        echo "✔️ Python3 installed successfully!"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
        echo "🔄 Windows detected. Checking for required tools..."
        
        # Check if winget is available (Windows 10 and later)
        if ! command_exists winget; then
            echo "❌ Winget is not available. Please ensure you're running Windows 10 or later."
            echo "ℹ️ You can install Python manually from https://www.python.org/downloads/"
            echo "ℹ️ Make sure to check 'Add Python to PATH' during installation"
            exit 1
        fi

        # Try to install Python using winget
        echo "🔄 Installing Python 3.13 using winget..."
        winget install Python.Python.3.13
        
        # Refresh PATH environment
        export PATH="$PATH:/c/Users/$USERNAME/AppData/Local/Programs/Python/Python313:/c/Users/$USERNAME/AppData/Local/Programs/Python/Python313/Scripts"
        
        # Verify Python installation
        if ! command_exists python3; then
            if command_exists python; then
                echo "✔️ Python is installed as 'python' instead of 'python3'"
                alias python3=python
                python --version
            else
                echo "❌ Python installation failed. Please install manually from https://www.python.org/downloads/"
                echo "ℹ️ Ensure to check 'Add Python to PATH' during installation"
                exit 1
            fi
        else
            python3 --version
        fi
        
        echo "✔️ Python installation completed!"
    else
        echo "❌ Unsupported OS. Please install Python3 manually."
        exit 1
    fi
else
    echo "✔️ Python3 is already installed."
fi

# 2. Check if Pipenv is installed
if ! command_exists pipenv; then
    echo "❌ Pipenv is not installed."
    echo "🔄 Installing Pipenv..."
    python3 -m pip install --user pipenv
    echo "✔️ Pipenv installed successfully!"
else
    echo "✔️ Pipenv is already installed."
fi

# 3. Verify the repository
if [ ! -d "./.git" ]; then
    echo "❌ This is not a Git repository. Please ensure you have cloned the repository before running this script."
    exit 1
else
    echo "✔️ Git repository verified."
fi

# 4. Install dependencies with Pipenv
if [ -f "Pipfile" ]; then
    echo "🔄 Installing dependencies from Pipfile..."
    pipenv install
    echo "✔️ Dependencies installed successfully!"
else
    echo "❌ Pipfile not found in the repository. Please check your setup."
    exit 1
fi

# 5. Activate the Pipenv virtual environment
echo "🔄 Activating the virtual environment..."
source "$(pipenv --venv)/bin/activate"
echo "✔️ Virtual environment activated! You are now in the Pipenv environment."

# 7. Prompt to configure Git user and email
echo "🔧 Configuration of Git user and email for this repository:"
read -p "👉 Enter your Git username: " git_user
read -p "👉 Enter your Git email: " git_email

git config user.name "$git_user"
git config user.email "$git_email"

echo "✔️ Git user and email have been configured."
echo "🎉 Project setup is complete! You are now inside the Pipenv shell."