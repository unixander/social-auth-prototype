# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

class SlackAPIMock(object):

    base_url = 'https://slack.com/api/'
    methods = {
        'oauth.access': {'ok': True, 'access_token': 'access_token'},
        'auth.test': {'ok': True, 'user_id': '123'},
        'chat.postMessage': {
            'ok': True,
            'channel': 'CNUMBER',
            'message': {
                'text': 'test',
                'username': 'Desk.Live bot',
                'type': 'message',
                'subtype': 'bot_message'
            }
        },
        'users.list': {
            'ok': True,
            'members':[{
                'is_owner': False,
                'status': None,
                'deleted': False,
                'id': 'U18K3JGR2',
                'tz_offset': -25200,
                'is_admin': False,
                'color': '4bbe2e',
                'is_bot': True,
                'is_primary_owner': False,
                'team_id': 'T18KBHTA5',
                'name': 'chatlio',
                'profile': {
                    'real_name': 'Chatlio',
                    'bot_id': 'B18HZBP9R',
                    'real_name_normalized': 'Chatlio',
                    'first_name': 'Chatlio',
                    'api_app_id': 'A03BS4Q25',
                },
                'tz_label': 'Pacific Daylight Time',
                'real_name': 'Chatlio',
                'is_restricted': False,
                'is_ultra_restricted': False,
                'tz': None
            }, {
                'is_owner': False,
                'status': None,
                'deleted': False,
                'id': 'U29J9NGTY',
                'tz_offset': -25200,
                'is_admin': False,
                'color': 'e7392d',
                'is_bot': True,
                'is_primary_owner': False,
                'team_id': 'T18KBHTA5',
                'name': 'desklive_local',
                'profile': {
                    'bot_id': 'B29JL7TPT',
                    'real_name_normalized': 'DeskLive Local',
                    'first_name': 'DeskLive Local',
                    'api_app_id': 'A1FVBFQJ1',
                    'real_name': 'DeskLive Local'
                },
                'tz_label': 'Pacific Daylight Time',
                'real_name': 'DeskLive Local',
                'is_restricted': False,
                'is_ultra_restricted': False,
                'tz': None
            }, {
                'is_owner': False,
                'status': None,
                'deleted': False,
                'id': 'U2DM27FJP',
                'tz_offset': -25200,
                'is_admin': False,
                'color': 'e96699',
                'is_bot': True,
                'is_primary_owner': False,
                'team_id': 'T18KBHTA5',
                'name': 'mrplannerdev',
                'profile': {
                    'bot_id': 'B2DNH8K54',
                    'avatar_hash': 'gecb83c95f4d',
                    'real_name_normalized': 'MrPlannerDev',
                    'first_name': 'MrPlannerDev',
                    'api_app_id': 'A2CEXN6QJ',
                    'real_name': 'MrPlannerDev'
                },
                'tz_label': 'Pacific Daylight Time',
                'real_name': 'MrPlannerDev',
                'is_restricted': False,
                'is_ultra_restricted': False,
                'tz': None
            }, {
                'is_owner': False,
                'status': None,
                'deleted': False,
                'id': 'U2A1EB4G5',
                'tz_offset': 10800,
                'is_admin': False,
                'color': '674b1b',
                'has_2fa': False,
                'is_bot': False,
                'is_primary_owner': False,
                'team_id': 'T18KBHTA5',
                'name': 'test_user',
                'profile': {
                    'last_name': 'User',
                    'avatar_hash': 'g56bc0d4a58e',
                    'real_name_normalized': 'Test User',
                    'first_name': 'Test',
                    'email': 'test_user@mailinator.com',
                    'real_name': 'Test User'
                },
                'tz_label': 'Moscow Time',
                'real_name': 'Test User',
                'is_restricted': False,
                'is_ultra_restricted': False,
                'tz': 'Europe/Moscow'
            }, {
                'is_owner': True,
                'status': None,
                'deleted': False,
                'id': 'U18K6UZDK',
                'tz_offset': 10800,
                'is_admin': True,
                'color': '9f69e7',
                'has_2fa': False,
                'is_bot': False,
                'is_primary_owner': True,
                'team_id': 'T18KBHTA5',
                'name': 'yershov',
                'profile': {
                    'last_name': 'Y',
                    'real_name_normalized': 'Alex Y',
                    'first_name': 'Alex',
                    'email': 'unixander@gmail.com',
                    'real_name': 'Alex Y'
                },
                'tz_label': 'Arabia Standard Time',
                'real_name': 'Alex Y',
                'is_restricted': False,
                'is_ultra_restricted': False,
                'tz': 'Asia/Kuwait'
            }, {
                'is_owner': False,
                'status': None,
                'deleted': False,
                'id': 'U2A1DAC7R',
                'tz_offset': 10800,
                'is_admin': False,
                'color': '3c989f',
                'has_2fa': False,
                'is_bot': False,
                'is_primary_owner': False,
                'team_id': 'T18KBHTA5',
                'name': 'yershov_mailinator',
                'profile': {
                    'last_name': 'Test',
                    'real_name_normalized': 'Test Test',
                    'first_name': 'Test',
                    'email': 'yershov@mailinator.com',
                    'real_name': 'Test Test'
                },
                'tz_label': 'Moscow Time',
                'real_name': 'Test Test',
                'is_restricted': False,
                'is_ultra_restricted': False,
                'tz': 'Europe/Moscow'
            }, {
                'is_owner': False,
                'status': None,
                'deleted': False,
                'id': 'USLACKBOT',
                'tz_offset': -25200,
                'is_admin': False,
                'color': '757575',
                'is_bot': False,
                'is_primary_owner': False,
                'team_id': 'T18KBHTA5',
                'name': 'slackbot',
                'profile': {
                    'last_name': '',
                    'avatar_hash': 'sv1444671949',
                    'real_name_normalized': 'slackbot',
                    'first_name': 'slackbot',
                    'real_name': 'slackbot',
                    'fields': None
                },
                'tz_label': 'Pacific Daylight Time',
                'real_name': 'slackbot',
                'is_restricted': False,
                'is_ultra_restricted': False,
                'tz': None
            }]
        }
    }

    @staticmethod
    def handle_post(*args, **kwargs):
        param = args[0]
        method = param.split('/')[-1]
        response = SlackAPIMock.methods.get(method, {'ok': False, 'message': 'error'})
        return response
