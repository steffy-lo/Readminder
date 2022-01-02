## Inspiration

As avid readers of comics and manga, we found it a hassle to constantly keep track of the latest chapters released or the current progress for comics that we're reading.
Even though there are many websites that allows users to create and manage their "To-Read" list, there are no reminders or notifications when the
lastest chapter of the comic is released. 

Instead of manually checking these websites to view the latest updates, we came up with a cool idea to build an automated email reminder that would send us the links to read where
we left off and let us know whenever our favourite comics release a new chapter.

And so, the automated reading reminder, READMINDER, is built!

## What it does

Readminder is an application that lets you schedule reminders based on your reading list and progress data on [Anime Planet](https://www.anime-planet.com/).
Users would be required to create an Anime Planet account in order to use Readminder.

Readminder sends an automated email and text reminder (scheduled through Windows task scheduler) of the latest chapter released for comics you are reading and a
respective link to read where you left off based on your progress tracked on [Anime Planet](https://www.anime-planet.com/).


## How we built it

Using Python and Selenium, we automated the process of manually searching up the latest chapter of the comics you are reading and checking where you
left off. Based on your Anime Planet account, we web scrape the comics from your reading list then check for new updates on a reading site with the chapter links.

Then, with the help of Twilio, we send the text notifications to the user and HTML email reminders via Python.

Finally, using Windows Task Scheduler, the app can send notifications based on the configured frequency such as daily, weekly or monthly.

> Note: Currently, we have only tested task scheduling and automating the reminders using Windows Task Scheduler. In the future, we plan to test on other OS machines.

### Built With
![Python](https://img.shields.io/badge/-Python-303030?style=for-the-badge&logo=python&logoColor=ffde24)
![Selenium](https://img.shields.io/badge/-Selenium-303030?style=for-the-badge&logo=selenium&logoColor=green)
![Twilio](https://img.shields.io/badge/-Twilio-303030?style=for-the-badge&logo=twilio&logoColor=red)

## Challenges we ran into

- Website detects our bot as malicious activity, found a workaround for this by tweaking the options of the webdriver
- Learning Selenium for the first time for this project
- Web scraping the right data from Anime Planet and a reading site to send the chapter updates and reading links to users

## Accomplishments that we're proud of

- Built an automation tool that can save hundreds of minutes of people's time

## What we learned

- Selenium as a useful webdriver tool to easily web scrape websites for this project
- Learned how to run Python scripts on Windows Task Scheduler to automate everyday needs like sending emails
- Used and learned about Twilio, its capabilities and features

## What's next for Readminder

- Improve robustness of the app, so it will support other websites and more variety of comics besides only manga
- Expand to other categories besides comics, such as tv shows, etc.
- Figure out how to automate the reminders on other OS devices besides Windows
- Send text reminders to other messaging apps like WhatsApp instead of just phone number
- Create the .exe application so non-developer-friendly so that anyone can set up the Python scripts


