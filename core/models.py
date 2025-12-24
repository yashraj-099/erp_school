from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import uuid

class Role(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self): return self.name

class User(AbstractUser):
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='core_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='core_user_set',
        related_query_name='user',
    )
class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    def __str__(self): return self.name
class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    def __str__(self): return self.name
class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, blank=True)
    def __str__(self): return self.name

    def clean(self):
        if self.user:
            # Check if user is associated with a student
            if Student.objects.filter(user=self.user).exists():
                raise ValidationError("This User is already associated with a Student.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    grade = models.CharField(max_length=50, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    def __str__(self): return self.name

    def clean(self):
        if self.user:
            # Check if user is associated with a teacher
            if Teacher.objects.filter(user=self.user).exists():
                raise ValidationError("This User is already associated with a Teacher.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
        
class FeeRecord(models.Model):
    STATUS_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    date = models.DateField()
    invoice_no = models.CharField(max_length=20, unique=True)
    def save(self, *args, **kwargs):
        if not self.invoice_no:
            self.invoice_no = f"INV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class Result(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)
    exam_date = models.DateField()
    
    class Meta:
        unique_together = ("student", "subject")
            
      

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    def __str__(self): return self.title
