from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


@receiver(user_signed_up)
def add_oauth_user_to_student_group(request, user, **kwargs):
    student_group = Group.objects.get(name='student')
    user.groups.add(student_group)
    user.save()
    