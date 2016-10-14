========================
Slack Team Authentication Prototype
========================

Description
-------------

Slack team authentication prototype implements flow for fetching Slack team members and invite them to join website.
When first member from team joins website, all other members are loaded to database and invites are sent to them.
When other team members join website they are associated with already loaded Slack Users.

Requirements:
-------------

- Python 3.x
- PostgreSQL
- redis-server (is used as celery broker)

Setup:
-------------

- create Slack app on api.slack.com and set callback url for Slack OAuth {domain}/complete/slack/
- Create database (defautl name is 'slack_auth_proto') and install requirements
- copy env.example to config/.env and fill variables
- Run celery worker: celery -A social_auth_proto.taskapp.celery worker --loglevel=info --concurrency=1
- run server locally: ./manage.py runserver
