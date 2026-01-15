# 🚀 Deployment Guide - Make Your App Live

## Overview
Deploy your Django app to make it accessible on Android devices as a PWA.

---

## ⭐ Option 1: PythonAnywhere (Easiest for Beginners)

### Why PythonAnywhere?
- ✅ Free tier available
- ✅ Django-friendly
- ✅ HTTPS included
- ✅ Easy setup
- ✅ No credit card needed

### Steps:

1. **Sign Up**
   - Visit: https://www.pythonanywhere.com
   - Create free account
   - Verify email

2. **Upload Your Code**
   ```bash
   # Option A: Upload as ZIP
   # Zip your project folder
   # Upload via Files tab
   
   # Option B: Use Git
   # In PythonAnywhere Bash console:
   git clone https://github.com/yourusername/yourrepo.git
   ```

3. **Create Virtual Environment**
   ```bash
   # In Bash console:
   mkvirtualenv --python=/usr/bin/python3.10 myenv
   cd ~/your-project-folder
   pip install -r requirements.txt
   ```

4. **Configure Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.10
   - Set source code path: `/home/yourusername/your-project-folder`
   - Set working directory: `/home/yourusername/your-project-folder`

5. **Configure WSGI File**
   - Click on WSGI configuration file link
   - Replace content with:
   ```python
   import os
   import sys
   
   path = '/home/yourusername/your-project-folder'
   if path not in sys.path:
       sys.path.append(path)
   
   os.environ['DJANGO_SETTINGS_MODULE'] = 'injection_moulding.settings'
   
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

6. **Update Django Settings**
   ```python
   # In settings.py:
   ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
   
   STATIC_ROOT = '/home/yourusername/your-project-folder/staticfiles'
   STATIC_URL = '/static/'
   
   # For production:
   DEBUG = False
   ```

7. **Collect Static Files**
   ```bash
   # In Bash console:
   cd ~/your-project-folder
   python manage.py collectstatic
   ```

8. **Setup Database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

9. **Reload Web App**
   - Go to Web tab
   - Click "Reload" button
   - Visit: https://yourusername.pythonanywhere.com

### Your App is Live! 🎉

---

## 🚀 Option 2: Heroku (Popular Choice)

### Why Heroku?
- ✅ Free tier (with credit card)
- ✅ Easy deployment
- ✅ Git-based workflow
- ✅ HTTPS included

### Steps:

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Prepare Your App**
   
   Create `Procfile`:
   ```
   web: gunicorn injection_moulding.wsgi
   ```
   
   Create `runtime.txt`:
   ```
   python-3.10.12
   ```
   
   Update `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   # Add: gunicorn
   ```

3. **Update Settings**
   ```python
   # settings.py
   import os
   
   ALLOWED_HOSTS = ['yourapp.herokuapp.com', 'localhost']
   
   # Static files
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   STATIC_URL = '/static/'
   
   # Database (use PostgreSQL on Heroku)
   import dj_database_url
   DATABASES = {
       'default': dj_database_url.config(
           default='sqlite:///db.sqlite3'
       )
   }
   ```

4. **Deploy**
   ```bash
   # Login to Heroku
   heroku login
   
   # Create app
   heroku create yourapp-name
   
   # Initialize git (if not already)
   git init
   git add .
   git commit -m "Initial commit"
   
   # Deploy
   git push heroku main
   
   # Run migrations
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   
   # Open app
   heroku open
   ```

### Your App is Live! 🎉

---

## 🌐 Option 3: Railway (Modern & Easy)

### Why Railway?
- ✅ Free tier ($5 credit/month)
- ✅ Very easy setup
- ✅ Modern interface
- ✅ HTTPS included

### Steps:

1. **Sign Up**
   - Visit: https://railway.app
   - Sign up with GitHub

2. **Deploy**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-detects Django
   - Click "Deploy"

3. **Configure**
   - Add environment variables in Railway dashboard
   - Set `ALLOWED_HOSTS`
   - Run migrations via Railway CLI

### Your App is Live! 🎉

---

## 🔧 Option 4: DigitalOcean (More Control)

### Why DigitalOcean?
- ✅ Full server control
- ✅ $5/month droplet
- ✅ Good performance
- ✅ Scalable

### Steps:

1. **Create Droplet**
   - Sign up at digitalocean.com
   - Create Ubuntu droplet
   - Choose $5/month plan

2. **Setup Server**
   ```bash
   # SSH into server
   ssh root@your-server-ip
   
   # Install dependencies
   apt update
   apt install python3-pip python3-venv nginx
   
   # Upload your code
   # Setup virtual environment
   # Configure Nginx
   # Setup Gunicorn
   # Configure SSL with Let's Encrypt
   ```

3. **Configure Domain**
   - Point domain to server IP
   - Setup SSL certificate

### Your App is Live! 🎉

---

## 📱 After Deployment: Install on Android

### For Users:

1. **Open Chrome on Android**
   - Visit your deployed URL
   - Example: https://yourusername.pythonanywhere.com

2. **Install App**
   - Chrome shows "Add to Home Screen" banner
   - Or tap menu (⋮) → "Add to Home Screen"
   - Tap "Add" or "Install"

3. **Use App**
   - App icon appears on home screen
   - Tap to open in full screen
   - Works like native app!

### Share with Team:

Send them:
1. Your app URL
2. Instructions: "Open in Chrome → Add to Home Screen"
3. Done!

---

## 🔒 Security Checklist

Before going live:

- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Use environment variables for secrets
- [ ] Setup HTTPS (automatic on most platforms)
- [ ] Change default SECRET_KEY
- [ ] Setup proper database (not SQLite for production)
- [ ] Configure CORS if needed
- [ ] Setup backup system
- [ ] Monitor error logs

---

## 📊 Monitoring & Maintenance

### Check App Health:
- Monitor error logs
- Check database size
- Monitor traffic
- Test on different devices

### Updates:
```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push

# For PythonAnywhere: Upload new files + reload
# For Heroku: git push heroku main
# For Railway: Auto-deploys on git push
```

---

## 💡 Tips for Production

1. **Use PostgreSQL** instead of SQLite
   ```bash
   pip install psycopg2-binary
   ```

2. **Setup Email** for notifications
   ```python
   # settings.py
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   ```

3. **Add Error Tracking**
   - Use Sentry for error monitoring
   - Setup logging

4. **Backup Database**
   - Regular automated backups
   - Test restore process

5. **Performance**
   - Enable caching
   - Optimize database queries
   - Compress static files

---

## 🆘 Troubleshooting

### Common Issues:

**Static files not loading:**
```bash
python manage.py collectstatic
# Check STATIC_ROOT and STATIC_URL settings
```

**Database errors:**
```bash
python manage.py migrate
# Check database configuration
```

**500 Server Error:**
- Check error logs
- Verify ALLOWED_HOSTS
- Check DEBUG setting

**App won't install on Android:**
- Verify HTTPS is working
- Check manifest.json is accessible
- Test in Chrome DevTools → Lighthouse

---

## 📞 Support Resources

### PythonAnywhere:
- Help: https://help.pythonanywhere.com
- Forum: https://www.pythonanywhere.com/forums/

### Heroku:
- Docs: https://devcenter.heroku.com
- Support: https://help.heroku.com

### Django:
- Docs: https://docs.djangoproject.com
- Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/

---

## ✅ Deployment Checklist

- [ ] Choose hosting platform
- [ ] Sign up for account
- [ ] Prepare app for deployment
- [ ] Update settings.py
- [ ] Create required files (Procfile, etc.)
- [ ] Deploy code
- [ ] Run migrations
- [ ] Create superuser
- [ ] Collect static files
- [ ] Test app in browser
- [ ] Test PWA installation on Android
- [ ] Share URL with users
- [ ] Setup monitoring
- [ ] Configure backups

---

## 🎉 Success!

Once deployed:
1. ✅ Your app is live on the internet
2. ✅ Accessible from any device
3. ✅ Can be installed on Android as PWA
4. ✅ Updates automatically when you push changes
5. ✅ Works offline with cached data

**Next:** Create app icons and test installation on Android device!
