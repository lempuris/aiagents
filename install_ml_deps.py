#!/usr/bin/env python3
"""
Install ML dependencies for predictive analysis
"""
import subprocess
import sys

def install_dependencies():
    """Install required ML packages"""
    packages = [
        'scikit-learn>=1.3.0',
        'numpy>=1.24.0'
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    print("\n🎉 All ML dependencies installed successfully!")
    print("You can now run the predictive analysis features.")
    return True

if __name__ == "__main__":
    install_dependencies()