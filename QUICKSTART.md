# Quick Start Guide

## Run Locally (Development)

1. **Activate virtual environment**
```bash
source venv/bin/activate
```

2. **Run the development server**
```bash
python manage.py runserver
```

3. **Access the application**
- Main site: http://localhost:8000
- Admin interface: http://localhost:8000/admin

## Default Admin Credentials

For testing purposes, an admin account has been created:

- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@thetatau.org`

**⚠️ IMPORTANT**: Change this password in production!

## Testing the Application

### Test Flow

1. **Sign in as Admin**
   - Go to http://localhost:8000
   - Click "Admin Sign In"
   - Use credentials above

2. **Create a Brother Account**
   - Click "Create New Account"
   - Email: `john.brother@example.com`
   - Role: Brother
   - Note the generated password

3. **Create a PNM Account**
   - Click "Create New Account"
   - Email: `jane.pnm@example.com`
   - Role: PNM
   - Note the generated password

4. **Sign in as Brother (in incognito/private window)**
   - Username: `john.brother`
   - Password: (from step 2)
   - Fill out profile with interests (e.g., "I love robotics, engineering, building things, coding Python, and playing soccer")
   - Upload a photo
   - View success page

5. **Sign in as PNM (in another incognito/private window)**
   - Username: `jane.pnm`
   - Password: (from step 3)
   - Fill out profile with similar interests (e.g., "I'm interested in engineering, love coding and robotics, enjoy soccer")
   - View matching results
   - Click "Schedule Coffee Chat"

### Sample Brother Profiles for Testing

Create multiple brothers with different interests:

**Brother 1: Tech Enthusiast**
```
Name: John Smith
Year: Junior
Major: Computer Science
Description: I'm passionate about software development, artificial intelligence, and machine learning. Love coding in Python and JavaScript. In my free time, I enjoy hackathons, gaming, and building side projects. I also play ultimate frisbee and love hiking.
```

**Brother 2: Business Leader**
```
Name: Mike Johnson
Year: Senior
Major: Business Administration
Description: Entrepreneurship is my passion! I love startups, business strategy, and leadership. Currently working on my own venture. Interests include networking, public speaking, and mentoring. Big fan of basketball and CrossFit.
```

**Brother 3: Environmental Engineer**
```
Name: David Lee
Year: Sophomore
Major: Environmental Engineering
Description: Dedicated to sustainability and fighting climate change. Love renewable energy, clean technology, and green building design. Hobbies include rock climbing, camping, photography, and volunteer work with local environmental groups.
```

## Deployment to Railway

### Quick Reference:
See **[RAILWAY_QUICK_START.md](RAILWAY_QUICK_START.md)** for fast-track deployment (~10 minutes)

### Complete Guide:
See **[RAILWAY_DEPLOYMENT_GUIDE.md](RAILWAY_DEPLOYMENT_GUIDE.md)** for detailed step-by-step instructions with:
- PostgreSQL database setup
- Environment variable configuration
- Admin account creation
- Troubleshooting guide
- Security checklist

Quick Railway setup:
1. Push code to GitHub
2. Connect Railway to your GitHub repo
3. Add PostgreSQL database in Railway
4. Set environment variables (DEBUG=False, SECRET_KEY, ALLOWED_HOSTS)
5. Deploy and create admin account!

## Troubleshooting

### "No such table" errors
```bash
python manage.py migrate
```

### Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Port already in use
```bash
python manage.py runserver 8001
```

### Module not found errors
```bash
pip install -r requirements.txt
```

## Key URLs

- Landing Page: `/`
- Login: `/login/`
- Logout: `/logout/`
- Dashboard: `/dashboard/` (redirects based on role)
- Admin Dashboard: `/admin-dashboard/`
- Create User: `/admin-dashboard/create-user/`
- Brother Profile: `/brother/profile/create/`
- Brother Success: `/brother/success/`
- PNM Profile: `/pnm/profile/create/`
- PNM Results: `/pnm/results/`

## Project Info

- **Framework**: Django 5.2+
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Matching**: scikit-learn TF-IDF + Cosine Similarity
- **UI**: Bootstrap 5 + Custom CSS
- **Colors**: Theta Tau Cherry Red (#C8102E) and Gold (#FFC72C)

Enjoy building connections with Theta Tau! 🤝

