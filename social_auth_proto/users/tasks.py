# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from social_auth_proto.users.slack_util import SlackApiHelper
from social_auth_proto.users.forms import SlackUserForm
from social_auth_proto.users.models import SlackUser, User
from social_auth_proto.taskapp.celery import app as celery_app


def process_members(json_members):
    """
    Fill member data from json data
    """
    for member in json_members:
        if member.get('is_bot') or member.get('name') == 'slackbot' or member.get('is_deleted')\
                or member.get('is_restricted') or member.get('is_ultra_restricted'):
            # Skip slackbot user, bot users, deleted users and guest users
            continue
        profile = member.get('profile', {})
        member_data = {
            'team': member.get('team_id'),
            'slack_id': member.get('id'),
            'name': member.get('name'),
            'real_name': member.get('real_name', ''),
            'email': profile.get('email', ''),
            'is_admin': member.get('is_admin', False),
            'is_owner': member.get('is_owner', False),
            'first_name': profile.get('first_name', ''),
            'last_name': profile.get('last_name', ''),
            'timezone': member.get('tz', ''),
            'commands_access': True
        }
        yield member_data


@celery_app.task(bind=True)
def update_team_members_list(self, user):
    """
    Fetch Slack teams data from user social data. Then fetches all slack members and send invite to all members.
    If Slack Member for current user already exists, then assign user to this Slack member
    """
    assert isinstance(user, User)
    site_url = Site.objects.get_current().domain
    socials = user.social_auth.filter(provider='slack')

    for social in socials:
        team_id = social.extra_data.get('team_id', '')
        token = social.extra_data.get('access_token', '')
        user_slack_id = social.extra_data.get('id', '')

        try:
            slack_user = SlackUser.objects.get(slack_id=user_slack_id, team=team_id)
        except SlackUser.DoesNotExist:
            pass
        else:
            # If slack user already exists, assign current user to it
            slack_user.user = user
            slack_user.save()
            return
        api_helper = SlackApiHelper(token=token, team_id=team_id)
        # Get team members
        json_members = api_helper.get_team_members_list()

        for member_data in process_members(json_members):
            # Check if member id is the same as initial user slack_id
            if member_data.get('slack_id') == user_slack_id:
                # Assign slack member to user
                member_data['user'] = user.id
            form = SlackUserForm(member_data)
            if form.is_valid():
                slack_user = form.save()
                if not slack_user.user_id:
                    message = render_to_string('slack/invite_message.html', context={'site_url': site_url})
                    time.sleep(1)  # Sleep to prevent Slack rate limit hit on multiple sending
                    api_helper.send_slackbot_message(channel=slack_user.slack_id, message=message)
