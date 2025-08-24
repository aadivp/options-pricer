# 🚀 Deployment Guide - Options Pricer Web App

This guide will help you deploy your Options Pricer application online for free using Streamlit Cloud.

## 📋 Prerequisites

1. **GitHub Account** (free)
2. **Streamlit Cloud Account** (free)
3. **All project files** (already created)

## 🎯 Quick Deployment Steps

### Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right and select "New repository"
3. Name it `options-pricer` or similar
4. Make it **Public** (required for free Streamlit Cloud)
5. Don't initialize with README (we already have files)
6. Click "Create repository"

### Step 2: Upload Your Code to GitHub

**Option A: Using GitHub Desktop (Recommended for beginners)**
1. Download and install [GitHub Desktop](https://desktop.github.com/)
2. Clone your repository
3. Copy all files from the "Options Pricer" folder to the repository folder
4. Commit and push to GitHub

**Option B: Using Git commands**
```bash
# Navigate to your project directory
cd "Options Pricer"

# Initialize git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Options Pricer web app"

# Add remote repository (replace with your GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/options-pricer.git

# Push to GitHub
git push -u origin main
```

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `YOUR_USERNAME/options-pricer`
5. Set the main file path: `streamlit_app.py`
6. Click "Deploy!"

## 📁 Required Files for Deployment

Make sure these files are in your GitHub repository:

```
options-pricer/
├── streamlit_app.py      # Main Streamlit application
├── formulas.py           # Black-Scholes calculations
├── requirements_web.txt  # Python dependencies
└── README.md            # Project documentation
```

## 🔧 Configuration Files

### requirements_web.txt
```
streamlit>=1.28.0
numpy>=1.21.0
scipy>=1.7.0
plotly>=5.0.0
matplotlib>=3.5.0
```

### .gitignore (optional but recommended)
```
__pycache__/
*.pyc
.DS_Store
.env
```

## 🌐 Alternative Free Deployment Options

### 1. **Render.com** (Free tier available)
- Similar to Streamlit Cloud
- Good for Python web apps
- Free tier includes 750 hours/month

### 2. **Railway.app** (Free tier available)
- Easy deployment
- Good for Python applications
- Free tier with usage limits

### 3. **Heroku** (Free tier discontinued, but still popular)
- More complex setup
- Requires credit card for verification
- Good for production apps

## 🚀 Local Testing Before Deployment

Test your app locally before deploying:

```bash
# Install dependencies
pip install -r requirements_web.txt

# Run the app locally
streamlit run streamlit_app.py
```

The app should open at `http://localhost:8501`

## 🔍 Troubleshooting Common Issues

### Issue: "Module not found" errors
**Solution**: Make sure all dependencies are in `requirements_web.txt`

### Issue: App won't deploy
**Solution**: 
1. Check that `streamlit_app.py` is the main file
2. Ensure repository is public
3. Verify all files are committed to GitHub

### Issue: Charts not displaying
**Solution**: Make sure Plotly is in requirements and properly imported

### Issue: Calculations not working
**Solution**: Test locally first, ensure `formulas.py` is in the same directory

## 📊 Monitoring Your App

Once deployed, you can:
- Monitor usage in Streamlit Cloud dashboard
- View logs for debugging
- Update by pushing new commits to GitHub
- Share the public URL with others

## 🔄 Updating Your App

To update your deployed app:
1. Make changes to your local files
2. Commit and push to GitHub
3. Streamlit Cloud will automatically redeploy

## 🌟 Features of Your Deployed App

Your web app will include:
- ✅ Interactive parameter sliders
- ✅ Real-time option price calculations
- ✅ Option Greeks (Delta, Gamma, Theta, Vega)
- ✅ Implied volatility calculator
- ✅ Sensitivity analysis charts
- ✅ Payoff diagrams
- ✅ Greeks visualization
- ✅ Mobile-responsive design
- ✅ Professional styling

## 📱 Accessing Your App

Once deployed, you'll get a URL like:
```
https://your-app-name.streamlit.app
```

You can share this URL with anyone to use your Options Pricer!

## 🎉 Success!

Your Options Pricer is now live on the web and accessible to anyone with the URL. The app will automatically update whenever you push changes to GitHub.

## 📞 Support

If you encounter issues:
1. Check the Streamlit Cloud logs
2. Test locally first
3. Verify all files are properly committed
4. Check the Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io) 