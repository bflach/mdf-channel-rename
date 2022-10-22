# Create virtual environment if not exists
$venv_folder = '.\venv\'
if (-Not (Test-Path -Path $venv_folder)) {
    Write-Output "Create virtual environment"
    python3 -m venv $venv_folder
} else { Write-Output "Environment exists!" }

# Activate virtual environment 
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Uninstall unnecessary packages
#pip uninstall -r not_requirements.txt -y

# Create binary file from script
#.\create_installer.ps1