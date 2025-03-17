from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_freelancer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    skills = models.CharField(max_length=500, null=True, blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    languages = models.CharField(max_length=200, null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    availability = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def is_profile_complete(self):
        if self.is_freelancer:
            # Required fields for freelancers
            required_fields = [
                self.bio,
                self.skills,
                self.hourly_rate,
                self.country,
                self.phone_number,
                self.languages,
                self.education,
                self.experience,
                self.availability
            ]
            return all(field for field in required_fields)
        else:
            # Required fields for clients
            required_fields = [
                self.bio,
                self.country,
                self.phone_number
            ]
            return all(field for field in required_fields)

class Project(models.Model):
    PROJECT_STATUS_CHOICES = [
        ('open', 'Open for Applications'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    DURATION_CHOICES = [
        ('short', 'Less than 1 month'),
        ('medium', '1-3 months'),
        ('long', '3-6 months'),
        ('ongoing', 'Ongoing')
    ]

    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Entry Level'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert')
    ]

    title = models.CharField(max_length=200)
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posted_projects')
    description = models.TextField()
    required_skills = models.CharField(max_length=500)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    budget_max = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES)
    status = models.CharField(max_length=20, choices=PROJECT_STATUS_CHOICES, default='open')
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateField(null=True, blank=True)
    assigned_freelancer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_projects')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class ProjectAttachment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='project_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.project.title}"

    class Meta:
        ordering = ['-uploaded_at']

class ProjectApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn')
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    freelancer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='project_applications')
    cover_letter = models.TextField()
    proposed_budget = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    estimated_duration = models.CharField(max_length=20, choices=Project.DURATION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Application for {self.project.title} by {self.freelancer.user.username}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['project', 'freelancer']  # Prevent multiple applications

class ProjectMilestone(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.project.title}"

    class Meta:
        ordering = ['due_date']
