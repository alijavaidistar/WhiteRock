from django.db import models
from django.conf import settings  # Import settings to use AUTH_USER_MODEL
from accounts.models import Unit
from django.utils import timezone  # Add if not already



class Request(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('returned', 'Returned'),
        ('approved', 'Approved'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    form_name = models.CharField(max_length=255)  
    data = models.JSONField()  
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    submitted_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='request_pdfs/', blank=True, null=True)  # PDF file if approved
    comments = models.TextField(blank=True, null=True)  # New field for admin comments
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)  # ✅ User Signature
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)  # ✅ NEW



    delegated_to = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="delegated_requests"
)

    delegated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="delegated_by_user"
    )

    delegated_at = models.DateTimeField(null=True, blank=True)


    approved_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='approved_requests'
)

    approved_at = models.DateTimeField(null=True, blank=True)



    returned_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='returned_requests'
)

    returned_at = models.DateTimeField(null=True, blank=True)






    def __str__(self):
        return f"{self.user.username} - {self.form_name} ({self.status})"
