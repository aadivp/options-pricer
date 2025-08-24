# 🔧 Troubleshooting Streamlit Cloud Deployment

## ❌ Error: "installer returned a non-zero exit code"

This error typically occurs due to dependency conflicts or missing packages. Here are the solutions:

## 🎯 Quick Fix - Try These Files

### Option 1: Use the Minimal App (Recommended)
1. **Use `app.py`** instead of `streamlit_app.py`
2. **Use `requirements.txt`** (the simple version)
3. **Deploy with main file**: `app.py`

### Option 2: Use the Full App with Fixed Requirements
1. **Use `streamlit_app.py`**
2. **Use `requirements_web.txt`** (with specific versions)
3. **Deploy with main file**: `streamlit_app.py`

## 📁 File Structure for Deployment

Make sure your GitHub repository has these files:

```
your-repo/
├── app.py              # Minimal version (recommended)
├── streamlit_app.py    # Full version with charts
├── requirements.txt    # Simple dependencies
├── requirements_web.txt # Specific versions
└── formulas.py         # Black-Scholes calculations
```

## 🔧 Step-by-Step Fix

### Step 1: Choose Your App Version

**For Minimal Version (Most Likely to Work):**
- Main file: `app.py`
- Requirements: `requirements.txt`

**For Full Version (With Charts):**
- Main file: `streamlit_app.py`
- Requirements: `requirements_web.txt`

### Step 2: Update Your Streamlit Cloud Settings

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Find your app
3. Click "Settings"
4. Update the main file path to match your choice above
5. Click "Save"

### Step 3: Redeploy

1. Make a small change to your code (add a comment)
2. Commit and push to GitHub
3. Streamlit Cloud will automatically redeploy

## 🐛 Common Issues and Solutions

### Issue 1: Import Errors
**Solution**: Use `app.py` which has all functions included directly

### Issue 2: Version Conflicts
**Solution**: Use `requirements.txt` with simple package names

### Issue 3: Missing Dependencies
**Solution**: Check that all required packages are in requirements file

### Issue 4: Python Version Issues
**Solution**: Streamlit Cloud uses Python 3.9 by default

## 📋 Requirements File Comparison

### Simple Version (`requirements.txt`)
```
streamlit
numpy
scipy
plotly
```

### Specific Versions (`requirements_web.txt`)
```
streamlit==1.48.1
numpy==2.3.2
scipy==1.16.1
plotly==6.3.0
matplotlib==3.10.5
```

## 🧪 Test Locally First

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Test minimal version
streamlit run app.py

# Test full version
streamlit run streamlit_app.py
```

## 🔍 Debug Steps

1. **Check Streamlit Cloud logs** for specific error messages
2. **Try the minimal version first** (`app.py`)
3. **Simplify requirements** to just essential packages
4. **Remove any custom imports** that might cause issues

## ✅ Success Checklist

- [ ] Repository is public
- [ ] Main file path is correct in Streamlit Cloud
- [ ] Requirements file is in the repository
- [ ] No syntax errors in the code
- [ ] All imports are standard Python packages

## 🆘 Still Having Issues?

1. **Try the minimal version** (`app.py`) first
2. **Check the deployment logs** in Streamlit Cloud
3. **Remove plotly temporarily** if charts aren't essential
4. **Use only numpy and scipy** for calculations

## 🎉 Expected Result

After successful deployment, you should see:
- ✅ App loads without errors
- ✅ Parameter sliders work
- ✅ Calculations update in real-time
- ✅ Charts display correctly (if using full version)

---

**Next**: Try deploying with `app.py` and `requirements.txt` for the best chance of success! 