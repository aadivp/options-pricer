#!/usr/bin/env python3
"""
Setup script for Options Pricer deployment
Checks all required files and prepares for deployment
"""

import os
import sys

def check_files():
    """Check if all required files exist"""
    required_files = [
        'streamlit_app.py',
        'formulas.py',
        'requirements_web.txt',
        'README.md'
    ]
    
    missing_files = []
    
    print("🔍 Checking required files...")
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    return missing_files

def check_dependencies():
    """Check if all dependencies are in requirements_web.txt"""
    print("\n📦 Checking dependencies...")
    
    if not os.path.exists('requirements_web.txt'):
        print("❌ requirements_web.txt not found")
        return False
    
    with open('requirements_web.txt', 'r') as f:
        requirements = f.read()
    
    required_packages = [
        'streamlit',
        'numpy',
        'scipy',
        'plotly'
    ]
    
    missing_packages = []
    for package in required_packages:
        if package not in requirements:
            missing_packages.append(package)
            print(f"❌ {package} not in requirements_web.txt")
        else:
            print(f"✅ {package}")
    
    return len(missing_packages) == 0

def create_gitignore():
    """Create .gitignore file if it doesn't exist"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/

# Environment variables
.env
.env.local
"""
    
    if not os.path.exists('.gitignore'):
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore")
    else:
        print("✅ .gitignore already exists")

def test_imports():
    """Test if all imports work correctly"""
    print("\n🧪 Testing imports...")
    
    try:
        import streamlit
        print("✅ streamlit")
    except ImportError:
        print("❌ streamlit - not installed")
        return False
    
    try:
        import numpy
        print("✅ numpy")
    except ImportError:
        print("❌ numpy - not installed")
        return False
    
    try:
        import scipy
        print("✅ scipy")
    except ImportError:
        print("❌ scipy - not installed")
        return False
    
    try:
        import plotly
        print("✅ plotly")
    except ImportError:
        print("❌ plotly - not installed")
        return False
    
    try:
        from formulas import blackScholes, calculate_implied_volatility
        print("✅ formulas module")
    except ImportError as e:
        print(f"❌ formulas module - {e}")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 Options Pricer - Deployment Setup")
    print("=" * 50)
    
    # Check files
    missing_files = check_files()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Create .gitignore
    create_gitignore()
    
    # Test imports
    imports_ok = test_imports()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Setup Summary:")
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        print("   Please create these files before deployment")
    else:
        print("✅ All required files present")
    
    if deps_ok:
        print("✅ Dependencies configured correctly")
    else:
        print("❌ Some dependencies missing from requirements_web.txt")
    
    if imports_ok:
        print("✅ All imports working correctly")
    else:
        print("❌ Some imports failed - install missing packages")
    
    # Next steps
    print("\n🎯 Next Steps:")
    print("1. If any issues above, fix them first")
    print("2. Create a GitHub repository")
    print("3. Upload your code to GitHub")
    print("4. Deploy on Streamlit Cloud")
    print("\n📖 See DEPLOYMENT_GUIDE.md for detailed instructions")
    
    if not missing_files and deps_ok and imports_ok:
        print("\n🎉 Your project is ready for deployment!")
        return True
    else:
        print("\n⚠️  Please fix the issues above before deploying")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 