# SimplyBridge Deployment Guide

## Current Structure
```
SIMPLYBRIDGE/
├── app/                    # Backend API
│   ├── main.py            # FastAPI app
│   ├── routes/           # API endpoints
│   ├── models/           # Database models
│   └── ...
├── frontend/             # Frontend HTML pages
│   ├── landing_page.html
│   ├── login.html
│   ├── register.html
│   ├── developer_dashboard.html
│   ├── developer_directory.html
│   └── developer_profile.html
├── .env                # Environment config
├── requirements.txt    # Python dependencies
└── DEPLOY.md          # This file
```

---

## Deploy to Render (RECOMMENDED)

Render is free and perfect for this setup. It can host both API and frontend.

### Step 1: Push to GitHub
```bash
# In your project folder:
git init
git add .
git commit -m "Initial SimplyBridge"

# Create repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/simplybridge.git
git push -u origin main
```

### Step 2: Deploy Backend on Render

1. Go to https://render.com → Sign up with GitHub
2. Click "New" → "Web Service"
3. Connect your GitHub repo
4. Configure:
   - **Name**: `simplybridge`
   - **Root Directory**: (leave empty)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables (click "Advanced"):
   - `DATABASE_URL`: `sqlite:///./simplybridge.db`
   - `SECRET_KEY`: `aV#9sK2$LpQ5mN8oR3tU7wX1yZ4cB6fE`
   - `FRONTEND_URL`: `https://simplybridge.onrender.com` (your domain)

6. Click "Deploy Web Service"

### Step 3: Update CORS (After deploy)
Once deployed, click on your service → "Environment" → Add:
```
FRONTEND_URL=https://your-app-name.onrender.com
```

### Step 4: Test
- API: `https://your-app-name.onrender.com`
- API Docs: `https://your-app-name.onrender.com/docs`
- Login: `https://your-app-name.onrender.com/login`

---

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# In browser, open:
http://127.0.0.1:8000/login
```

---

## Netlify Alternative (Frontend Only)

If you just want frontend:
1. Copy all `.html` files from `frontend/` folder
2. Go to https://netlify.com/drag-drop
3. Drop the files
4. Done!

Note: For Netlify, you'll need the API on Render.

---

## Common Issues

**CORS Error**: Update `FRONTEND_URL` in Render environment variables

**Database Error**: Render has ephemeral filesystem - use their PostgreSQL addon for production

**Static Files**: The app serves HTML from `frontend/` folder automatically