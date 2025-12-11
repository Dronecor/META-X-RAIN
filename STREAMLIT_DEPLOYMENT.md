# Streamlit Admin Deployment Guide

## Overview
This guide covers deploying the ShopBuddy Admin interface to Streamlit Cloud.

## Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- Backend deployed and accessible (e.g., on Render)

## Backend URL
Your backend is deployed at: `https://shopbuddy-mk97.onrender.com/api/v1`

## Deployment Steps

### 1. Prepare Your Repository
Ensure all changes are committed and pushed to GitHub:
```bash
git add .
git commit -m "feat: Streamlit admin deployment configuration"
git push origin main
```

### 2. Configure Streamlit Secrets
In Streamlit Cloud, you'll need to add secrets. The secrets should match this format:

```toml
# Backend API URL
BACKEND_API_URL = "https://shopbuddy-mk97.onrender.com/api/v1"

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "your_secure_password_here"
```

### 3. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository: `Dronecor/META-X-RAIN`
4. Set the main file path: `frontend_admin/app.py`
5. Click "Advanced settings"
6. Add the secrets from step 2 in the "Secrets" section
7. Click "Deploy"

### 4. Post-Deployment Configuration

#### Add Secrets in Streamlit Cloud Dashboard:
1. Go to your app settings
2. Navigate to "Secrets" section
3. Paste the configuration:
   ```toml
   BACKEND_API_URL = "https://shopbuddy-mk97.onrender.com/api/v1"
   ADMIN_USERNAME = "admin"
   ADMIN_PASSWORD = "your_secure_password_here"
   ```
4. Save changes

### 5. Verify Deployment

Once deployed, test the following:
- [ ] App loads without errors
- [ ] Login works with your credentials
- [ ] Dashboard shows conversations (if any exist)
- [ ] Product Management tab loads
- [ ] Can add new products
- [ ] Can view product inventory

## Local Development

For local development, the app will use environment variables from `.env`:

```bash
# .env
BACKEND_API_URL=http://localhost:8000/api/v1
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin
```

Run locally:
```bash
streamlit run frontend_admin/app.py
```

## Troubleshooting

### Connection Refused Error
**Error**: `Connection refused` or `Max retries exceeded`

**Solution**: Ensure `BACKEND_API_URL` is set correctly in Streamlit secrets:
- Should be: `https://shopbuddy-mk97.onrender.com/api/v1`
- NOT: `http://localhost:8000/api/v1`

### Authentication Issues
**Error**: Cannot log in

**Solution**: 
1. Check that `ADMIN_USERNAME` and `ADMIN_PASSWORD` are set in secrets
2. Verify credentials match what you're entering
3. Check Streamlit logs for specific error messages

### CORS Issues
**Error**: CORS policy blocking requests

**Solution**: Ensure your backend (Render deployment) has CORS configured to allow requests from your Streamlit app domain.

## File Structure

```
.streamlit/
├── config.toml              # Theme and server settings (committed)
├── secrets.toml             # Sensitive config (NOT committed)
└── secrets.toml.example     # Template (committed)

frontend_admin/
└── app.py                   # Main Streamlit app
```

## Security Notes

1. **Never commit `secrets.toml`** - It's in `.gitignore`
2. **Use strong passwords** for `ADMIN_PASSWORD`
3. **Rotate credentials** regularly
4. **Use HTTPS** for backend URL (already configured)

## Configuration Priority

The app reads configuration in this order:
1. Streamlit secrets (for deployment)
2. Environment variables (for local dev)
3. Default values (fallback)

## Requirements

The app will automatically install dependencies from `requirements.txt`. Ensure it includes:
```
streamlit
requests
pandas
```

## Next Steps

After deployment:
1. Share the Streamlit app URL with your team
2. Set up proper admin credentials
3. Monitor app performance in Streamlit Cloud dashboard
4. Configure custom domain (optional, Streamlit Cloud Pro)

## Support

- Streamlit Docs: https://docs.streamlit.io
- Streamlit Community: https://discuss.streamlit.io
- Backend (Render): https://dashboard.render.com
