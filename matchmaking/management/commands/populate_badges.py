from django.core.management.base import BaseCommand
from matchmaking.models import Badge


class Command(BaseCommand):
    help = 'Populate the database with Theta Tau badges based on image files'

    def handle(self, *args, **kwargs):
        # Define all badges based on actual image files
        badges_data = [
            # Brotherhood badges
            {
                'name': 'Artistic',
                'pillar': 'BROTHERHOOD',
                'description': 'Interests in arts, music, and creative activities',
                'icon_image': 'images/badges/brotherhood-artistic.png',
                'order': 1
            },
            {
                'name': 'Fitness',
                'pillar': 'BROTHERHOOD',
                'description': 'Sports, exercise, and physical activities',
                'icon_image': 'images/badges/brotherhood-fitness.png',
                'order': 2
            },
            {
                'name': 'Brotherhood',
                'pillar': 'BROTHERHOOD',
                'description': 'General brotherhood values and activities',
                'icon_image': 'images/badges/brotherhood-og.png',
                'order': 3
            },
            {
                'name': 'Outdoors',
                'pillar': 'BROTHERHOOD',
                'description': 'Hiking, camping, and outdoor adventures',
                'icon_image': 'images/badges/brotherhood-outdoors.png',
                'order': 4
            },
            
            # Professionalism badges
            {
                'name': 'Career Development',
                'pillar': 'PROFESSIONALISM',
                'description': 'Focus on professional growth and career advancement',
                'icon_image': 'images/badges/profession-career.png',
                'order': 1
            },
            {
                'name': 'Finance',
                'pillar': 'PROFESSIONALISM',
                'description': 'Finance, business, and economics expertise',
                'icon_image': 'images/badges/profession-finance.png',
                'order': 2
            },
            {
                'name': 'Professionalism',
                'pillar': 'PROFESSIONALISM',
                'description': 'General professional development and skills',
                'icon_image': 'images/badges/profession-og.png',
                'order': 3
            },
            {
                'name': 'Technical Skills',
                'pillar': 'PROFESSIONALISM',
                'description': 'Engineering, coding, and technical expertise',
                'icon_image': 'images/badges/profession-technical.png',
                'order': 4
            },
            
            # Service badges
            {
                'name': 'Community Service',
                'pillar': 'SERVICE',
                'description': 'Local volunteer work and community involvement',
                'icon_image': 'images/badges/service-community.png',
                'order': 1
            },
            {
                'name': 'Environmental',
                'pillar': 'SERVICE',
                'description': 'Sustainability and green initiatives',
                'icon_image': 'images/badges/service-environment.png',
                'order': 2
            },
            {
                'name': 'Service',
                'pillar': 'SERVICE',
                'description': 'General service activities and volunteer work',
                'icon_image': 'images/badges/service-og.png',
                'order': 3
            },
            {
                'name': 'Outreach',
                'pillar': 'SERVICE',
                'description': 'Community outreach programs and engagement',
                'icon_image': 'images/badges/service-outreach.png',
                'order': 4
            },
        ]
        
        # Create or update badges
        created_count = 0
        updated_count = 0
        
        for badge_data in badges_data:
            badge, created = Badge.objects.update_or_create(
                name=badge_data['name'],
                pillar=badge_data['pillar'],
                defaults={
                    'description': badge_data['description'],
                    'icon_image': badge_data['icon_image'],
                    'order': badge_data['order'],
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created badge: {badge.name} ({badge.get_pillar_display()})')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Updated badge: {badge.name} ({badge.get_pillar_display()})')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary: Created {created_count} badges, Updated {updated_count} badges'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total badges in database: {Badge.objects.count()}')
        )
