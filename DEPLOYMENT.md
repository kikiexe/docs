# 🚀 Deployment Guide - ZK-Yield Documentation

This guide will help you deploy the ZK-Yield documentation to Vercel.

## Prerequisites

- ✅ Git repository initialized
- ✅ GitHub account
- ✅ Vercel account ([Sign up free](https://vercel.com/signup))

---

## Step 1: Commit Changes

```bash
# Add all new files
git add .

# Commit changes
git commit -m "feat: Update documentation for ZK-Yield

- Restructure sidebar for ZK-Yield
- Add ZK Circuits section
- Add DeFi Strategies section
- Add Developer Guide
- Update intro with ZK-Yield messaging
- Add comprehensive README
"

# Push to GitHub
git push origin main
```

---

## Step 2: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Recommended)

1. **Go to Vercel**

   - Visit [vercel.com](https://vercel.com)
   - Click "Add New Project"

2. **Import Git Repository**

   - Select "Import Git Repository"
   - Choose your GitHub repository
   - Click "Import"

3. **Configure Project**

   ```
   Framework Preset: Docusaurus
   Root Directory: ./
   Build Command: npm run build
   Output Directory: build
   Install Command: npm install
   ```

4. **Environment Variables** (if needed)

   - No environment variables needed for documentation

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your site will be live!

### Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy: Y
# - Which scope: (select your account)
# - Link to existing project: N
# - Project name: zk-yield-docs
# - Directory: ./
# - Want to override settings: N

# Deploy to production
vercel --prod
```

---

## Step 3: Configure Custom Domain (Optional)

### In Vercel Dashboard

1. Go to your project settings
2. Click "Domains"
3. Add your custom domain
4. Update DNS records at your domain provider:
   ```
   Type: CNAME
   Name: docs (or @)
   Value: cname.vercel-dns.com
   ```

---

## Step 4: Enable Automatic Deployments

Vercel automatically deploys on every push to `main` branch:

- **Production**: Deploys from `main` branch
- **Preview**: Deploys from feature branches
- **Each commit** gets a unique preview URL

### Disable Auto-Deploy (if needed)

In Vercel project settings:

1. Go to "Git"
2. Uncheck "Auto-Deploy"

---

## Step 5: Verify Deployment

### Check These Pages

- ✅ Homepage: `https://your-site.vercel.app/`
- ✅ Docs: `https://your-site.vercel.app/docs/intro`
- ✅ ZK Circuits: `https://your-site.vercel.app/docs/zk-circuits/introduction`
- ✅ DeFi Strategies: `https://your-site.vercel.app/docs/defi-strategies/overview`

### Test Features

- ✅ Sidebar navigation works
- ✅ Search functionality
- ✅ Dark/Light mode toggle
- ✅ Mobile responsive
- ✅ All links work

---

## Deployment Checklist

Before going live, verify:

- [ ] All markdown files render correctly
- [ ] No broken links
- [ ] Images load properly
- [ ] Search works
- [ ] Sidebar structure correct
- [ ] Mobile view looks good
- [ ] Analytics configured (optional)
- [ ] Custom domain configured (if applicable)

---

## Continuous Integration

### GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Documentation

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install dependencies
        run: npm install

      - name: Build documentation
        run: npm run build

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          vercel-args: "--prod"
```

---

## Troubleshooting

### Build Fails

**Error**: `Module not found`

```bash
# Solution: Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Error**: `Build exceeded maximum duration`

```bash
# Solution: Optimize build
# In docusaurus.config.ts, disable unused plugins
```

### Sidebar Not Updating

**Solution**: Clear browser cache or hard refresh (Ctrl+Shift+R)

### Search Not Working

**Solution**: Rebuild search index

```bash
npm run build
# Vercel will automatically index on deploy
```

---

## Performance Optimization

### Enable Compression

Vercel automatically compresses:

- ✅ Gzip compression
- ✅ Brotli compression
- ✅ Image optimization

### Configure Headers

Create `vercel.json`:

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

---

## Analytics (Optional)

### Google Analytics

In `docusaurus.config.ts`:

```typescript
gtag: {
  trackingID: 'G-XXXXXXXXXX',
}
```

### Vercel Analytics

```bash
npm i @vercel/analytics

# Add to app
import { Analytics } from '@vercel/analytics/react';
```

---

## Maintenance

### Update Documentation

```bash
# Edit markdown files
# Commit and push
git add .
git commit -m "docs: update content"
git push

# Vercel auto-deploys!
```

### Monitor Deployments

- Vercel Dashboard → Deployments
- See build logs
- Rollback if needed

---

## Next Steps

After deployment:

1. **Share the link** with your team
2. **Set up analytics** to track usage
3. **Add to README** in main repo
4. **Update Discord/Twitter** with docs link
5. **Create feedback form** for improvements

---

## URLs

After deployment, you'll have:

- **Production**: `https://zk-yield-docs.vercel.app`
- **Preview**: `https://zk-yield-docs-git-<branch>.vercel.app`
- **Latest**: `https://zk-yield-docs-<hash>.vercel.app`

---

## Support

Need help deploying?

- 📖 [Vercel Docs](https://vercel.com/docs)
- 📖 [Docusaurus Deployment](https://docusaurus.io/docs/deployment)
- 💬 [Vercel Discord](https://vercel.com/discord)

---

**Ready to deploy? Follow the steps above!** 🚀
