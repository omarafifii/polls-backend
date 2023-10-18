# Backend for Polls Voting System

This repo is the backend for a voting app written in react. When the user opens the link they will see a list of topics which they can vote on. To vote on a topic the user will click on it and then enter their email. An OTP will be sent to their email. After entering their OTP successfully the vote will be count.

### Useful Links

Deployment: https://voting-backend.omarafifi.com/

Backend Github: https://github.com/omarafifii/polls-frontend

### To access admin panel

username: admin

password: admin

### To run local smtp server to test emails for development

run this command in a new shell:
```bash
$ python -m aiosmtpd -n -l localhost:8025
```

### To install dependancies

run this command in a new shell:
```bash
$ pip install -r requirements.txt
```
