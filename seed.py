import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_manager.settings')
django.setup()

from django.contrib.auth.models import User
from events.models import Category, Event, Registration, UserProfile

def run_seed():
    print("Seeding database...")

    # 1. Users
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@eventhub.com', 'is_staff': True, 'is_superuser': True}
    )
    admin_user.set_password('admin123')
    admin_user.save()
    p_admin, _ = UserProfile.objects.get_or_create(user=admin_user)
    p_admin.role = 'ORGANIZER'
    p_admin.save()

    demo_user, _ = User.objects.get_or_create(
        username='alex_dev',
        defaults={'email': 'alex@example.com', 'first_name': 'Alex', 'last_name': 'Morgan'}
    )
    demo_user.set_password('demo123')
    demo_user.save()
    p_alex, _ = UserProfile.objects.get_or_create(user=demo_user)
    p_alex.role = 'ATTENDEE'
    p_alex.save()

    sarah_user, _ = User.objects.get_or_create(
        username='sarah_organizer',
        defaults={'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Conner'}
    )
    sarah_user.set_password('demo123')
    sarah_user.save()
    p_sarah, _ = UserProfile.objects.get_or_create(user=sarah_user)
    p_sarah.role = 'ORGANIZER'
    p_sarah.save()

    # 2. Categories
    cat_tech, _ = Category.objects.get_or_create(
        name='Technology',
        slug='technology',
        defaults={'icon': 'fa-laptop-code', 'description': 'Software, AI, Web Development & Tech Innovations'}
    )

    cat_design, _ = Category.objects.get_or_create(
        name='Design & UX',
        slug='design-ux',
        defaults={'icon': 'fa-palette', 'description': 'UI/UX Design, Graphics, Product & Motion Design'}
    )

    cat_music, _ = Category.objects.get_or_create(
        name='Music & Arts',
        slug='music-arts',
        defaults={'icon': 'fa-music', 'description': 'Live Concerts, Acoustic Nights & Art Exhibits'}
    )

    cat_business, _ = Category.objects.get_or_create(
        name='Business & Startups',
        slug='business-startups',
        defaults={'icon': 'fa-chart-line', 'description': 'Pitch Competitions, Leadership & Networking Summits'}
    )

    now = timezone.now()

    # 3. Events
    events_data = [
        {
            'title': 'AI & Future Tech World Summit 2026',
            'category': cat_tech,
            'organizer': admin_user,
            'location': 'Silicon Innovation Hub, San Francisco / Live Stream',
            'start_time': now + timedelta(days=5, hours=3),
            'end_time': now + timedelta(days=5, hours=8),
            'capacity': 150,
            'image_url': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=1200&q=80',
            'description': 'Explore groundbreaking advancements in Generative AI, Autonomous Agents, and Quantum Computing. Featuring keynote talks from industry leaders, interactive hackathons, and networking sessions.'
        },
        {
            'title': 'Modern UI/UX Design System Workshop',
            'category': cat_design,
            'organizer': sarah_user,
            'location': 'Design Lab Center, New York',
            'start_time': now + timedelta(days=12, hours=2),
            'end_time': now + timedelta(days=12, hours=6),
            'capacity': 40,
            'image_url': 'https://images.unsplash.com/photo-1542744094-3a3172720189?auto=format&fit=crop&w=1200&q=80',
            'description': 'A hands-on masterclass on crafting scalable design systems, glassmorphism aesthetics, accessible color palettes, and interactive prototypes.'
        },
        {
            'title': 'Indie Rock & Neon Acoustic Festival',
            'category': cat_music,
            'organizer': sarah_user,
            'location': 'Skyline Outdoor Arena, Austin, TX',
            'start_time': now + timedelta(days=18, hours=6),
            'end_time': now + timedelta(days=18, hours=11),
            'capacity': 300,
            'image_url': 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=1200&q=80',
            'description': 'An evening of live acoustic performances, indie pop bands, light shows, and gourmet food trucks under the stars.'
        },
        {
            'title': 'Startup Founder Pitch Night & Angels Meetup',
            'category': cat_business,
            'organizer': admin_user,
            'location': 'Venture Co-Working Lounge, Chicago',
            'start_time': now + timedelta(days=25, hours=4),
            'end_time': now + timedelta(days=25, hours=7),
            'capacity': 60,
            'image_url': 'https://images.unsplash.com/photo-1515187029135-18ee286d815b?auto=format&fit=crop&w=1200&q=80',
            'description': 'Early-stage tech founders present 5-minute pitches to venture capitalists and angel investors. Network over drinks and appetizers.'
        },
        {
            'title': 'Global Cloud Native & DevOps Conference',
            'category': cat_tech,
            'organizer': sarah_user,
            'location': 'International Tech Center, Seattle, WA',
            'start_time': now - timedelta(days=3),
            'end_time': now - timedelta(days=3, hours=-6),
            'capacity': 200,
            'image_url': 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=1200&q=80',
            'description': '[Past Event] Deep dive into Kubernetes, Terraform, microservices architectures, and serverless deployments.'
        }
    ]

    for data in events_data:
        event, created = Event.objects.get_or_create(
            title=data['title'],
            defaults=data
        )
        if created:
            print(f"Created event: {event.title}")

    # 4. Registrations
    e1 = Event.objects.first()
    if e1:
        Registration.objects.get_or_create(
            user=demo_user,
            event=e1,
            defaults={'tickets_count': 2, 'status': 'CONFIRMED'}
        )
        print(f"Registered demo user for: {e1.title}")

    print("Seeding completed successfully!")

if __name__ == '__main__':
    run_seed()
