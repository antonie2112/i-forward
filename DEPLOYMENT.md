# Deployment Guide: I.Forward to Vercel via GitHub

Follow these simple steps to move your project to the cloud.

### 1. Create a GitHub Repository
1. Go to [github.com/new](https://github.com/new).
2. Name it `iforward-sales-hub` (or whatever you like).
3. Do **not** initialize with README or .gitignore (we already have them!).
4. Copy the remote URL (e.g., `https://github.com/your-user/iforward-sales-hub.git`).

### 2. Push Your Code
In your local terminal (where the project is):
```bash
git add .
git commit -m "feat: Initial PWA transformation with Firebase Auth"
git remote add origin YOUR_GITHUB_URL
git push -u origin main
```

### 3. Connect to Vercel
1. Go to [vercel.com/new](https://vercel.com/new).
2. Import your `iforward-sales-hub` repository.
3. In **Build Settings**:
   - Framework Preset: `Other` (Vite will be auto-detected).
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. **Environment Variables**: Add your Firebase keys if you haven't put them in the code yet.
5. Click **Deploy**.

### 4. Continuous Deployment
Every time you `git push` to your GitHub repository, Vercel will automatically rebuild and redeploy your app!
