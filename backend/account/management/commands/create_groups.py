"""
Copyright 2023 The Scorch Authors.

Custom command to create the baseline Group and Users.
"""

from getpass import getpass

from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission

from account.models import Account

# Default Groups to create
# Groups have the following structure:
#     group_name: {
#         permission_name: [list of actions]
#     }
_groups = {
    'Administrators': {
        'log entry' : ['add','delete','change','view'],
        'group' : ['add','delete','change','view'],
        'permission' : ['add','delete','change','view'],
        'user' : ['add','delete','change','view'],
        'content type' : ['add','delete','change','view'],
        'session' : ['add','delete','change','view'],

        'entity type': ['add', 'delete', 'change', 'view'],
        'entity': ['add', 'delete', 'change', 'view'],
        'attribute': ['add', 'delete', 'change', 'view'],
        'attribute value': ['add', 'delete', 'change', 'view'],
        'scorecard': ['add', 'delete', 'change', 'view'],
        'scorecard version': ['add', 'delete', 'change', 'view'],
        'score level': ['add', 'delete', 'change', 'view'],
        'scoring item level': ['add', 'delete', 'change', 'view'],
        'scoring item': ['add', 'delete', 'change', 'view'],
        'scoring item version': ['add', 'delete', 'change', 'view'],
        'response': ['add', 'delete', 'change', 'view'],
        'scoring item response': ['add', 'delete', 'change', 'view'],
        'task': ['add', 'delete', 'change', 'view'],
    },

    'Entity Managers': {
        'entity type': ['add', 'delete', 'change', 'view'],
        'entity': ['add', 'delete', 'change', 'view'],
        'attribute': ['add', 'delete', 'change', 'view'],
        'attribute value': ['add', 'delete', 'change', 'view'],
    },

    'Scorecard Managers': {
        'scorecard': ['add', 'delete', 'change', 'view'],
        'scorecard version': ['add', 'delete', 'change', 'view'],
        'score level': ['add', 'delete', 'change', 'view'],
        'scoring item level': ['add', 'delete', 'change', 'view'],
        'scoring item': ['add', 'delete', 'change', 'view'],
        'scoring item version': ['add', 'delete', 'change', 'view'],
    },

    'Score Item Owners': {
        'scoring item': ['change', 'view'],
        'scoring item version': ['add', 'delete', 'change', 'view'],
    },

    'Responders': {
        'response': ['add', 'delete', 'change', 'view'],
        'scoring item response': ['add', 'delete', 'change', 'view'],
        'task': ['add', 'delete', 'change', 'view'],
    },

    'Reviewer': {
        'scoring item response': ['add', 'delete', 'change', 'view'],
        'task': ['add', 'delete', 'change', 'view'],
    },

    'Viewers': {
        'entity type': ['view'],
        'entity': ['view'],
        'attribute': ['view'],
        'attribute value': ['view'],
        'scorecard': ['view'],
        'scorecard version': ['view'],
        'score level': ['view'],
        'scoring item level': ['view'],
        'scoring item': ['view'],
        'scoring item version': ['view'],
        'scoring item': ['view'],
        'scoring item version': ['view'],
        'response': ['view'],
        'scoring item response': ['view'],
        'task': ['view'],
    },
}

# TODO: Move this to another command that loads "staff" users some other
#       way since we have to deal with secrets.
# Users have the structure:
#     username: {
#         'create': True,
#         'email': 'user@example.com', # required if create is True
#         'groups': [
#             'group_name 1',
#             'group_name 2'
#         ]
#     }

_users = {
    'admin': {
        'create': False,
        'groups': ['Administrators'],
    },
    # 'AnotherUser': {
    #     'create': True,
    #     'email': 'user@example.com',
    #     'groups': [
    #         'group_name 1',
    #         'group_name 2'
    #     ]
    # },
}


class Command(BaseCommand):

    help = 'Creates default Groups and Users'

    def handle(self, *args, **options):
        for group_name, group_info in _groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            curr_perms = group.permissions.all()
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'\nCreated group {group_name}'))
            else:
                self.stdout.write(f'\nModifying group {group_name}')
            for subject, actions in group_info.items():
                for action in actions:
                    name = f'Can {action} {subject}'
                    try:
                        perm = Permission.objects.get(name=name)
                        if perm in curr_perms:
                            self.stdout.write(
                                f' - Permission {name} already present')
                        else:
                            group.permissions.add(perm)
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f' - Added permission {name}'))
                    except Permission.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                               f'Permission not found: "{name}". Skipping.'))

            for user_name, user_info in _users.items():
                user = None
                if user_info['create']:
                    user, created = Account.objects.get_or_create(
                        username=user_name, is_staff=True,
                        email=user_info['email'])
                    if created:
                        matched = False
                        while not matched:
                            password = getpass(
                                prompt=f'Enter password for new user '
                                '{user_name}: ')
                            password_check = getpass(
                                prompt=f'Re-enter password: '
                            )
                            matched = (password == password_check)
                            if not matched:
                                self.stdout.write(
                                    self.style.WARNING(
                                        'Password do not match. Try again.'))
                        user.set_password(password)
                        user.save()
                        self.stdout.write(
                            self.style.SUCCESS(
                                f' - Created new user {user_name}'))
                else:
                    try:
                        user = Account.objects.get(username=user_name)
                        self.stdout.write(
                            f' - Located user {user_name}')
                    except Account.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                               f'User not found: "{user_name}". Skipping.'))

                if str(group) in user_info['groups']:
                    group_users = group.user_set.all()
                    if user not in group_users:
                        group.user_set.add(user)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f' - Added {user_name} to {group}'))
                    else:
                        self.stdout.write(
                            f' - User {user_name} already in {group}')

