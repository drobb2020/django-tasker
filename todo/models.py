from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


def user_directory_path(instance, filename):
    """
    Generate file path for user avatars.

    Parameters:
    - instance (Profile): The Profile instance associated with the user.
    - filename (str): The original filename of the uploaded file.

    Returns:
    str: The file path for storing the user's avatar.
    """
    return 'users/avatars/{0}/{1}'.format(instance.user.id, filename)


class Task(models.Model):
    """
    Represents a task in the application.

    Attributes:
    - title (str): The title of the task.
    - content (str): The content or description of the task.
    - is_completed (bool): Indicates whether the task is completed or not.
    - date_created (datetime): The date and time when the task was created.
    - date_updated (datetime): The date and time when the task was last updated.
    """
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_due = models.DateField(blank=True, null=True)
    date_completed = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the author and task.

        Returns:
        str: The  author and title of the task.
        """
        return f"{self.author} - {self.title}"


class Review(models.Model):
    """
    Represents a review associated with a task.

    Attributes:
    - reviewer_name (str): The name of the reviewer.
    - review_title (str): The title of the review.
    - task (Task): The associated task (foreign key relationship).
    - review_notes (str): Additional notes or comments for the review.
    """
    reviewer_name = models.CharField(max_length=100)
    review_title = models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    review_notes = models.TextField(max_length=250, default="To be added")

    def __str__(self):
        """
        Returns a string representation of the review.

        Returns:
        str: The title of the review.
        """
        return self.review_title


class Profile(models.Model):
    """
    Represents a user profile associated with a Django User.

    Attributes:
    - user (User): The associated Django User.
    - avatar (ImageField): The user's avatar image.
    - email (EmailField): The user's email address.
    - phone (PhoneNumberField): The user's phone number.
    - bio (str): The user's biography.
    - favorite_quote (str): The user's favorite quote.
    - quote_author (str): The author of the favorite quote.
    - quote_source (str): The source of the favorite quote.
    - social_facebook (URLField): Facebook profile URL.
    - social_linkedin (URLField): LinkedIn profile URL.
    - social_github (URLField): GitHub profile URL.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path, default='users/avatar-200.jpg')
    email = models.EmailField(max_length=128)
    phone = PhoneNumberField()
    bio = models.TextField(max_length=250)
    favorite_quote = models.CharField(max_length=255)
    quote_author = models.CharField(max_length=150, default="Anon")
    quote_source = models.CharField(max_length=100, default="Anon")
    social_facebook = models.URLField()
    social_linkedin = models.URLField()
    social_github = models.URLField()

    def __str__(self):
        """
        Returns a string representation of the user profile.

        Returns:
        str: The username of the associated Django User.
        """
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal receiver to create a user profile when a new user is created.

    Parameters:
    - sender: The sender of the signal (User model).
    - instance (User): The instance of the user being created.
    - created (bool): Indicates whether the user instance is newly created.
    - kwargs (dict): Additional keyword arguments.

    Returns:
    None
    """
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)
