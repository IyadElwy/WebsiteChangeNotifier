# WebsiteChangeNotifier

## Program to monitor a Website for changes and get notified by email when a change is Detected.
### Optionally search for specific regular expressions on Websites

### Requirements:
- Wget on your default OS
  - For Windows: [Click Here To Download Wget](https://eternallybored.org/misc/wget/)
  - Linux and Mac has it pre-installed 

### Dependencies:
  - os
  - random
  - subprocess (instead of os)
  - time
  - Rich
  - smtplib
  - ssl
  - MIMEText
  - MIMEMultipart
  - pyinputplus
  - inputimeout
  - datetime
  - re


## Version 2.0 introduces a Command Line UI for a more user friendly approach:
![Command Prompt 7_26_2021 2_41_38 AM](https://user-images.githubusercontent.com/83036619/126919155-3a345df4-1784-47b9-a473-514331576853.png)

![Command Prompt 7_26_2021 2_42_47 AM](https://user-images.githubusercontent.com/83036619/126919163-e68d0915-59fc-4beb-995d-ef22b96a1872.png)

![Command Prompt 7_26_2021 2_43_01 AM](https://user-images.githubusercontent.com/83036619/126919176-0987034b-7198-430c-a5c3-f615e498ad52.png)

![Wget  100%  http___www example com_ 7_26_2021 2_43_34 AM](https://user-images.githubusercontent.com/83036619/126919187-c6011375-41c1-4cca-95be-b63a271f488b.png)

![Command Prompt 7_27_2021 10_02_32 PM](https://user-images.githubusercontent.com/83036619/127219979-d3d2b9e1-ea8f-4209-b7f9-545cb17c2af5.png)

### How to use version 1.0:
```python
if __name__ == '__main__':
    file = Website(link="Any Website Link",
                   email_address="TEST@email.com", password="PASSWORD",
                   message_to_send="Your site changed!") # initialize the Website object to be monitored
    file.start_monitoring(5, True) #check for change every 5 seconds, if second param set to True a copy of the site will be sent via email

```

#### Works with static Websites that do not change dynamically
#### Html is sent optionally by email as boiler plate without resources
