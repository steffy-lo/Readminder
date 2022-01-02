## Inspiration

As avid readers of comics and manga, we found it a hassle to constantly keep track of the latest chapters released or the current progress for comics that we're reading.
Even though there are many websites that allows users to create and manage their "To-Read" list, there are no reminders or notifications when the
lastest chapter of the comic is released. 

Instead of manually checking these websites to view the latest updates, we came up with a cool idea to build an automated email reminder that would send us the links to read where
we left off and let us know whenever our favourite comics release a new chapter.

And so, the automated reading reminder, READMINDER, is built!

## What it does

Readminder is an application lets you schedule reminders based on your reading list and progress data on [Anime Planet](https://www.anime-planet.com/).
Users would be required to create an Anime Planet account in order to use Readminder.

Readminder sends an automated email and text reminder (scheduled through Windows task scheduler) of the latest chapter released for comics you are reading and a
respective link to read where you left off based on your progress tracked on Anime Planet (https://www.anime-planet.com/).


## How we built it

Using Python and Selenium, we automated the process of manually searching up the latest chapter of the comics you are reading and checking where you
left off


### Built With
![Python](https://img.shields.io/badge/-Python-303030?style=for-the-badge&logo=python&logoColor=ffde24)
![Selenium](https://img.shields.io/badge/-Selenium-303030?style=for-the-badge&logo=selenium&logoColor=green)

## Challenges we ran into

    Website detects our bot as malicious activity, found a workaround for this by tweaking the options of the webdriver

## Accomplishments that we're proud of

    Built an automation tool that can save hundreds of minutes of people's time

## What we learned

    Selenium with Python and the power of automation

## What's next for Readminder

    Improve robustness
    Expand to other categories besides comics


