import os
import django

# Setup Django (IMPORTANT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # 🔁 change if needed
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")

if email and password and username:
    if not User.objects.filter(email=email).exists():
        print("Creating superuser...")
        User.objects.create_superuser(
            email=email,
            username=username,
            password=password
        )
        print("✅ Superuser created")
    else:
        print("⚠️ Superuser already exists")
else:
    print("❌ Missing superuser environment variables")