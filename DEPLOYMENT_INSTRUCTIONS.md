
# Admin Frontend Deployment

1. **Deploy to Vercel**:
    - Go to Vercel Dashboard
    - Click "Add New Project"
    - Import the repository
    - Env Variables:
        - `NEXT_PUBLIC_BACKEND_API_URL`: Your deployed backend URL (e.g. `https://your-backend-app.vercel.app/api/v1`)
    - Click Deploy

2. **Backend Update**:
    - Ensure your backend `ALLOWED_ORIGINS` includes your new admin frontend URL.

# Customer Frontend Deployment

- Same as above, but Root Directory is `.` (root) or wherever your customer frontend is (it seems to be `app` or mixed in root).
- If customer frontend is the Next.js app in root, just deploy root.

# Twilio Integration

1. **Webhook**: Point Twilio Sandbox Webhook to `https://your-backend-app.vercel.app/api/v1/whatsapp/webhook`
2. **Opt-in**:
    - Users must send "join [sandbox-code]" first (Twilio rule).
    - Then they must type "YES" or "START" to opt-in to the bot logic as per your request.
    - Standard messages will be visually searched if image is attached.
