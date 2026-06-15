# TechFix Pro - Professional Repair Shop Website

Ek dum professional mobile aur electronics repair shop website!

## 📁 Project Structure

```
repair-shop-website/
├── index.html      (HTML structure)
├── style.css       (Responsive dark theme styling)
├── script.js       (Interactive features)
└── README.md       (This file)
```

## 🚀 GitHub Codespace Setup

### Step 1: Create Repository
1. GitHub par jaa
2. New repository create kar (e.g., `repair-shop-website`)
3. Clone ya Open in Codespace select kar

### Step 2: Files Add Kar
1. Codespace open hone ke baad
2. Upload karo ya copy-paste kar:
   - `index.html`
   - `style.css`
   - `script.js`

### Step 3: Live Server Start Kar
Codespace mein Terminal open kar (Ctrl + `)

```bash
# Python 3 se server start kar
python -m http.server 8000

# Ya Node.js http-server use kar
npm install -g http-server
http-server
```

Phir **Ports** tab par jaa aur port 8000 ko open kar.

## 🎨 Features

✅ **Modern Dark Theme** - Blue, Teal, Yellow colors
✅ **Fully Responsive** - Mobile, Tablet, Desktop
✅ **Smooth Animations** - Scroll animations, hover effects
✅ **Mobile Menu** - Hamburger menu for small screens
✅ **Contact Form** - Working form with validation
✅ **Fast Loading** - Lightweight CSS & JS
✅ **Professional Icons** - Tabler Icons CDN

## 📱 Sections

1. **Navigation** - Sticky navbar with mobile menu
2. **Hero** - Catchy headline with CTA button
3. **Services** - Mobile & Electronics repair cards
4. **Why Us** - 4 key benefits with icons
5. **Contact** - Form + Contact information
6. **Footer** - Links aur copyright

## 🔧 Customization Tips

### Business Details Change Karein:
`index.html` mein search kar:
- `TechFix Pro` → Apna shop name
- `+91 98765 43210` → Apna phone
- `contact@techfixpro.com` → Apna email
- `Main Street, Patna, Bihar` → Apna address

### Colors Change Karein:
`style.css` mein `--primary-color`, `--secondary-color` etc change kar

### Services Add/Remove:
`index.html` mein service cards ko duplicate ya delete kar

## 📝 Form Integration

Currently form sirf browser mein data show karta hai. Production ke liye:
1. Backend API connect kar (Node.js, PHP, Python)
2. Email service use kar (SendGrid, Mailgun)
3. Database store kar (MongoDB, MySQL)

Form validation already included hai!

## 🌐 Deploy Karne Ke Liye

### Option 1: GitHub Pages (Free)
```bash
git add .
git commit -m "Initial commit"
git push origin main
```
Settings → Pages → main branch select kar

### Option 2: Netlify
1. netlify.com par signup kar
2. Deploy karne ke liye GitHub repo connect kar
3. Auto-deploy on every push

### Option 3: Vercel
1. vercel.com par signup kar
2. Import project
3. Deploy ho jayega instantly!

## 🐛 Common Issues & Fixes

**Issue**: CORS error
**Fix**: Same origin se serve kar (localhost:8000)

**Issue**: Icons nahi dikh rahe
**Fix**: Internet connection check kar (CDN se load hote hain)

**Issue**: Mobile menu nahi khul raha
**Fix**: Console mein check kar (F12 → Console)

## 📞 Support

Koi issue aaye toh terminal mein check kar:
```bash
# Console errors dekh
# Network tab check kar
# Mobile responsive test kar (F12 → Toggle device toolbar)
```

## 🎯 Next Steps

1. ✅ GitHub Codespace mein setup kar
2. ✅ Apne business details add kar
3. ✅ Colors aur content customize kar
4. ✅ Live preview test kar
5. ✅ Deploy kar (GitHub Pages / Netlify / Vercel)
6. ✅ Domain connect kar (optional)

## 📊 Tech Stack

- **HTML5** - Semantic markup
- **CSS3** - Modern responsive design
- **Vanilla JavaScript** - No frameworks needed
- **Tabler Icons** - Beautiful SVG icons
- **CDN** - Fast loading

---

**Made with ❤️ for your repair shop business**

Koi question ho toh pooch na! 🙌
