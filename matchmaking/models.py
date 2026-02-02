from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class Badge(models.Model):
    """
    Badge model representing interests related to Theta Tau's three pillars.
    """
    PILLAR_CHOICES = [
        ('BROTHERHOOD', 'Brotherhood'),
        ('PROFESSIONALISM', 'Professionalism'),
        ('SERVICE', 'Service'),
    ]
    
    name = models.CharField(max_length=100)
    pillar = models.CharField(max_length=20, choices=PILLAR_CHOICES)
    description = models.TextField(help_text="Admin reference description")
    icon_image = models.CharField(max_length=200, default='images/badges/default.png', help_text="Path to badge icon image (e.g., 'images/badges/mentorship.png')")
    order = models.IntegerField(default=0, help_text="Display order within pillar")
    
    class Meta:
        ordering = ['pillar', 'order', 'name']
        unique_together = ['pillar', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_pillar_display()})"


class CustomUser(AbstractUser):
    """
    Custom User model with role-based access.
    Roles: ADMIN, BROTHER, PNM
    """
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('BROTHER', 'Brother'),
        ('PNM', 'PNM'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='PNM'
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class BrotherProfile(models.Model):
    """
    Profile for Brother users with photo and detailed information.
    """
    YEAR_CHOICES = [
        ('FRESHMAN', 'Freshman'),
        ('SOPHOMORE', 'Sophomore'),
        ('JUNIOR', 'Junior'),
        ('SENIOR', 'Senior'),
        ('GRADUATE', 'Graduate'),
    ]
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='brother_profile'
    )
    name = models.CharField(max_length=200)
    year = models.CharField(max_length=20, choices=YEAR_CHOICES)
    major = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='brother_photos/', blank=True, null=True)
    description = models.TextField(
        validators=[MinLengthValidator(20)],
        help_text="Tell PNMs about yourself, your interests, hobbies, career goals, etc."
    )
    badges = models.ManyToManyField(
        Badge,
        blank=True,
        related_name='brothers',
        help_text="Select badges that represent your interests"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.year} {self.major}"


class PNMProfile(models.Model):
    """
    Profile for PNM (Potential New Member) users.
    """
    YEAR_CHOICES = [
        ('FRESHMAN', 'Freshman'),
        ('SOPHOMORE', 'Sophomore'),
        ('JUNIOR', 'Junior'),
        ('SENIOR', 'Senior'),
        ('GRADUATE', 'Graduate'),
    ]
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='pnm_profile'
    )
    name = models.CharField(max_length=200)
    year = models.CharField(max_length=20, choices=YEAR_CHOICES)
    major = models.CharField(max_length=200)
    description = models.TextField(
        validators=[MinLengthValidator(20)],
        help_text="Describe your interests, hobbies, career goals, and what you're looking for in a brother connection."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.year} {self.major}"
