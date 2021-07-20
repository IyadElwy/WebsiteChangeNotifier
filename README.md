# WebsiteChangeNotifier

## Program to monitor a Website for changes and get notified by email when a change is Detected.

### Requirements:
- Wget on your default OS
  - For Windows: [Click Here To Download Wget](https://eternallybored.org/misc/wget/)
  - Linux and Mac has it pre-installed 

### Dependencies:
  - os
  - time
  - smtplib
  - ssl
  -  email.mime.text from MIMEText
  -  email.mime.multipart from MIMEMultipart



### How to use:
```python
if __name__ == '__main__':
    file = Website(link="Any Website Link",
                   email_address="TEST@email.com", password="PASSWORD",
                   message_to_send="Your site changed!") # initialize the Website object to be monitored
    file.start_monitoring(5, True) #check for change every 5 seconds, if second param set to True a copy of the site will be sent via email

```
