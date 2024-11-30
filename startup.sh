#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Starting project setup..."

# 1. Check if Python is installed
if ! command_exists python3; then
    echo "Python3 is not installed."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Installing Python3 on macOS..."
        if ! command_exists brew; then
            echo "Homebrew is not installed. Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
        echo "You're on Windows. Please install Python manually from https://www.python.org/downloads/"
        echo "Ensure Python3 and pip are added to your PATH after installation."
        exit 1
    else
        echo "Unsupported OS. Please install Python3 manually."
        exit 1
    fi
else
    echo "Python3 is already installed."
fi

# 2. Check if Pipenv is installed
if ! command_exists pipenv; then
    echo "Pipenv is not installed. Installing Pipenv..."
    python3 -m pip install --user pipenv
else
    echo "Pipenv is already installed."
fi

# 3. Clone the GitHub repo and navigate to the project directory
if [ ! -d "./.git" ]; then
    echo "Please ensure you have cloned the repository before running this script."
    exit 1
fi

# 4. Install dependencies with Pipenv
if [ -f "Pipfile" ]; then
    echo "Installing dependencies from Pipfile..."
    pipenv install
else
    echo "Pipfile not found in the repository. Please check your setup."
    exit 1
fi

# 5. Prompt to configure Git user and email
echo "Configuration of Git user and email for this repository:"
read -p "Enter your Git username: " git_user
read -p "Enter your Git email: " git_email

git config user.name "$git_user"
git config user.email "$git_email"

echo "Git user and email have been configured."
echo "Project setup is complete!"
