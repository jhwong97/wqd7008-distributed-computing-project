# List of packages to be included in requirements.txt
packages = [
    "requests",
    "pandas",
    "beautifulsoup4",
    "python-dotenv",
    "urllib3",
    "typing",
    "fredapi",
    "imfpy",
    "matplotlib",
    "seaborn",
    "pmdarima",
    "statsmodels",
    "scikit-learn",
    "python-dateutil"
]

# Path to the requirements.txt file
file_path = '/home/ubuntu/requirements.txt'

# Function to append missing packages to the file
def append_missing_packages(existing_packages):
    with open(file_path, 'a') as file:
        for package in packages:
            if package not in existing_packages:
                file.write(package + '\n')
                print(f"Appended {package} to {file_path}")

try:
    # Try to open the file in read mode
    with open(file_path, 'r') as file:
        existing_packages = file.read().splitlines()
        # Check for missing packages and append them
        print(f"Checking for missing packages...")
        append_missing_packages(existing_packages)
        print(f"Done updating requirements.txt file.")
        
except FileNotFoundError:
    # If the file does not exist, create it and write the packages
    with open(file_path, 'w') as file:
        file.write('\n'.join(packages) + '\n')
        print(f"Created {file_path} with specified packages.")
