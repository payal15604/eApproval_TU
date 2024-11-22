from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, null=True, blank=True)  # Temporarily store OTP if needed

    def __str__(self):
        return self.email
    
class NOCRequest(models.Model):
    student_name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=15)  # Add roll number
    email = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Foreign key to UserProfile
    request_description = models.TextField()
    google_drive_link = models.URLField()

    def __str__(self):
        return f"NOC Request from {self.student_name} ({self.roll_no})"

class NoDueSlip(models.Model):
    student_name = models.CharField(max_length=100)  # Name of the student
    roll_no = models.CharField(max_length=150)  # Roll number
    email = models.EmailField()  # Email address
    hostel = models.CharField(max_length=100, default= 'Hostel Name Not Provided')  # Name of the hostel
    room_no = models.CharField(max_length=100, default= 'Room Number Not Provided')  # Room number

    def _str_(self):
        return f"No Due Slip - {self.student_name} ({self.roll_no})"

class LORRequest(models.Model):
    student_name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=15)  # Add roll number
    email = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Foreign key to UserProfile
    request_description = models.TextField()
    google_drive_link = models.URLField()

    def __str__(self):
        return f"LOR Request from {self.student_name} ({self.roll_no})"
