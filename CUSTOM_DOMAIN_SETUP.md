# Custom Domain Setup Guide

**Custom Domain**: `data.theshipsagent.xyz`
**GitHub Pages URL**: `https://theshipsagent.github.io/panjiva-classification-system/`

---

## ✅ Step 1: CNAME File Created

The CNAME file has been created and pushed to GitHub:
- File: `CNAME`
- Content: `data.theshipsagent.xyz`
- Status: ✅ Committed and pushed

---

## 🌐 Step 2: Configure DNS Settings

You need to add a DNS record with your domain registrar (where you manage theshipsagent.xyz).

### DNS Configuration

**Login to your domain registrar** (e.g., GoDaddy, Namecheap, Cloudflare, etc.)

**Add CNAME Record**:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| CNAME | `data` | `theshipsagent.github.io` | 3600 (or Auto) |

### Common Registrars

**GoDaddy**:
1. Go to: DNS Management
2. Click: Add Record
3. Type: CNAME
4. Name: `data`
5. Value: `theshipsagent.github.io`
6. Save

**Namecheap**:
1. Go to: Advanced DNS
2. Add New Record
3. Type: CNAME Record
4. Host: `data`
5. Value: `theshipsagent.github.io`
6. Save

**Cloudflare**:
1. Go to: DNS → Records
2. Add record
3. Type: CNAME
4. Name: `data`
5. Target: `theshipsagent.github.io`
6. Proxy status: DNS only (gray cloud)
7. Save

### Verification

After adding the DNS record, verify it's propagating:

```bash
# Check CNAME record
nslookup data.theshipsagent.xyz

# Or use online tool
# https://dnschecker.org
```

DNS propagation takes **5-60 minutes** (sometimes up to 24 hours).

---

## 📄 Step 3: Enable GitHub Pages

1. **Go to GitHub Repository Settings**:
   ```
   https://github.com/theshipsagent/panjiva-classification-system/settings/pages
   ```

2. **Configure Pages**:
   - **Source**: Deploy from a branch
   - **Branch**: `main` (or select `gh-pages` if it exists)
   - **Folder**: `/ (root)`

3. **Custom Domain**:
   - GitHub should automatically detect your CNAME file
   - The field should show: `data.theshipsagent.xyz`
   - If not shown, manually enter: `data.theshipsagent.xyz`

4. **HTTPS**:
   - ✅ Check: "Enforce HTTPS" (after DNS propagates)
   - GitHub will automatically provision SSL certificate

5. **Click**: Save

---

## ⏱️ Step 4: Wait for Deployment

### Initial Deployment
- First deployment: **2-5 minutes**
- DNS propagation: **5-60 minutes**
- SSL certificate: **5-10 minutes** after DNS propagates

### Check Deployment Status

1. Go to repository **Actions** tab:
   ```
   https://github.com/theshipsagent/panjiva-classification-system/actions
   ```

2. Look for: "Deploy Documentation to GitHub Pages" workflow
3. Status should be: ✅ Green check mark

---

## 🎉 Step 5: Verify Your Live Site

Once DNS propagates and GitHub Pages deploys:

**Your dashboards will be live at**:
```
https://data.theshipsagent.xyz
```

**Test these URLs**:
- Main landing page: `https://data.theshipsagent.xyz/`
- Pipeline dashboard: `https://data.theshipsagent.xyz/classification_pipeline_dashboard.html`
- Technical flow: `https://data.theshipsagent.xyz/classification_technical_dataflow.html`
- Master plan: `https://data.theshipsagent.xyz/PIPELINE_MASTER_PLAN_UPDATED.md`

---

## 🔗 Step 6: Link from Homepage

Add a link on `theshipsagent.xyz` to your new data portal:

### Simple Link

```html
<a href="https://data.theshipsagent.xyz" target="_blank">
  View Data Models & Analytics →
</a>
```

### Styled Button

```html
<a href="https://data.theshipsagent.xyz"
   class="btn btn-primary"
   target="_blank">
  📊 Explore Data Models
</a>
```

### Navigation Menu Item

```html
<nav>
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/services">Services</a></li>
    <li><a href="https://data.theshipsagent.xyz">Data Models</a></li>
    <li><a href="/contact">Contact</a></li>
  </ul>
</nav>
```

### Hero Section

```html
<section class="hero">
  <h1>Maritime Data Analytics</h1>
  <p>Comprehensive cargo classification system for Panjiva import data</p>
  <a href="https://data.theshipsagent.xyz" class="cta-button">
    View Interactive Dashboards →
  </a>
</section>
```

---

## 🔧 Troubleshooting

### Issue: "Domain is improperly configured"

**Solution**:
1. Check DNS record is correct: `nslookup data.theshipsagent.xyz`
2. Wait for DNS propagation (up to 24 hours)
3. Verify CNAME points to: `theshipsagent.github.io`

### Issue: "Certificate not provisioned"

**Solution**:
1. Uncheck "Enforce HTTPS" temporarily
2. Wait 5-10 minutes
3. Re-check "Enforce HTTPS"
4. GitHub will provision certificate automatically

### Issue: "404 Not Found"

**Solution**:
1. Check GitHub Actions deployment succeeded
2. Verify files exist in repository
3. Check `index.html` exists (auto-created by workflow)
4. Try accessing directly: `https://data.theshipsagent.xyz/INDEX.html`

### Issue: DNS Not Propagating

**Check propagation status**:
```bash
# Windows
nslookup data.theshipsagent.xyz

# Or use online tool
https://dnschecker.org
```

**Force DNS refresh** (local machine):
```bash
# Windows
ipconfig /flushdns

# Mac/Linux
sudo dscacheutil -flushcache
```

---

## 📊 SEO Optimization (Optional)

Add metadata to your homepage for better search visibility:

```html
<head>
  <meta name="description" content="Panjiva maritime cargo classification system with interactive dashboards">
  <meta property="og:title" content="The Ships Agent - Data Models">
  <meta property="og:description" content="Interactive maritime data analytics and cargo classification">
  <meta property="og:url" content="https://data.theshipsagent.xyz">
  <meta property="og:type" content="website">
</head>
```

---

## 🔄 Future Updates

Whenever you push changes to the `build_documentation/` folder:

1. **Commit changes**:
   ```bash
   git add build_documentation/
   git commit -m "Update: dashboard improvements"
   git push
   ```

2. **GitHub Actions automatically**:
   - Runs deployment workflow
   - Updates `data.theshipsagent.xyz`
   - No manual steps needed!

3. **Live in 2-3 minutes**

---

## 📧 DNS Records Summary

Here's what your DNS should look like:

```
Type    Name    Value                         TTL
-----------------------------------------------------
CNAME   data    theshipsagent.github.io      3600
A       @       [Your main site IP]          3600
CNAME   www     theshipsagent.xyz            3600
```

---

## ✅ Checklist

Complete these steps in order:

- [x] CNAME file created in repository
- [x] CNAME file committed and pushed to GitHub
- [ ] DNS CNAME record added at registrar
- [ ] DNS propagation verified (5-60 minutes)
- [ ] GitHub Pages enabled in repository settings
- [ ] Custom domain configured in GitHub Pages
- [ ] HTTPS enforcement enabled
- [ ] Deployment workflow succeeded
- [ ] Site accessible at data.theshipsagent.xyz
- [ ] Link added to main homepage

---

## 🎯 Expected Timeline

| Step | Time |
|------|------|
| Push CNAME to GitHub | ✅ Complete |
| Add DNS record | 5 minutes (manual) |
| DNS propagation | 5-60 minutes |
| GitHub Pages deploy | 2-5 minutes |
| SSL certificate | 5-10 minutes |
| **Total** | **~20-80 minutes** |

---

## 📞 Support

If you encounter issues:

1. **Check GitHub Actions**: https://github.com/theshipsagent/panjiva-classification-system/actions
2. **Check GitHub Pages settings**: Settings → Pages
3. **Verify DNS**: https://dnschecker.org
4. **GitHub Pages docs**: https://docs.github.com/en/pages

---

**Last Updated**: 2026-01-13
**Status**: CNAME file pushed, awaiting DNS configuration
