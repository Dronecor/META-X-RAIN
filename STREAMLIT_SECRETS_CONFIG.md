# Streamlit Cloud Secrets Configuration

## 🚀 Quick Setup for Streamlit Cloud

### Step 1: Go to Your Streamlit Cloud App
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Find your deployed app or create a new one
3. Click on the **⚙️ Settings** button (three dots menu)
4. Select **"Secrets"**

### Step 2: Add These Secrets

Copy and paste **EXACTLY** this into the Secrets section:

```toml
# Backend API URL - Your Render deployment
BACKEND_API_URL = "https://shopbuddy-mk97.onrender.com/api/v1"

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"
```

### Step 3: Save and Reboot
1. Click **"Save"**
2. The app will automatically restart
3. Wait for it to redeploy (usually takes 30-60 seconds)

### Step 4: Test
1. Open your Streamlit Cloud app URL
2. Login with:
   - Username: `admin`
   - Password: `admin`
3. The Dashboard should now load conversations from your Render backend

---

## 🔧 Troubleshooting

### If you still see "Connection refused" error:

1. **Check the secrets are saved correctly**
   - Go back to Settings → Secrets
   - Verify the URL is exactly: `https://shopbuddy-mk97.onrender.com/api/v1`
   - No trailing slashes, no typos

2. **Check your Render backend is running**
   - Visit: https://shopbuddy-mk97.onrender.com/api/v1/docs
   - You should see the FastAPI documentation page
   - If not, your backend might be sleeping (Render free tier)

3. **Check CORS settings on backend**
   - Your backend needs to allow requests from Streamlit Cloud domain
   - Check `backend/main.py` for CORS configuration

4. **Force restart the Streamlit app**
   - In Streamlit Cloud, click "Reboot app"
   - This ensures it picks up the new secrets

---

## 📝 Important Notes

- **Never commit** `.streamlit/secrets.toml` to GitHub (it's in `.gitignore`)
- **Use strong passwords** in production (change from "admin")
- **Secrets are environment-specific**: Local uses `.streamlit/secrets.toml`, Cloud uses the web interface
- **Changes to secrets** require app restart to take effect

---

## 🎯 Current Configuration

- **Backend URL**: https://shopbuddy-mk97.onrender.com/api/v1
- **Frontend (Next.js)**: Deployed on Vercel
- **Admin (Streamlit)**: Deploy on Streamlit Cloud
- **Database**: SQLite (local) or PostgreSQL (production)

---

## 🔐 Security Recommendations

For production deployment:

1. Change `ADMIN_PASSWORD` to a strong password
2. Consider adding environment-based authentication
3. Use HTTPS for all connections (already configured)
4. Rotate credentials regularly
5. Consider using Streamlit's built-in authentication features

---

## 📞 Support

If issues persist:
- Check Streamlit Cloud logs (Settings → Logs)
- Verify backend is accessible: `curl https://shopbuddy-mk97.onrender.com/api/v1/admin/conversations`
- Check this repo's issues or create a new one
