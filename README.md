## Web scraping
##### _Scraping job posts on www.hellowork.com_
---
### Goals
    - get jobs from the website
    - automate scraping
    - automate daily mailing

### Usage
    sh run_scraper.sh
    
### Technology stack
    - Cron
    - Shell
    - Python3 (requests, BeautifulSoup, email, smtplib, ssl)

### Note
My Crontab as an example: 0  9,18  *  *  1-5  sh /my_path/run_scraper.sh
So my program gets jobs and sends me an email with results every weekday at 9am and 6pm