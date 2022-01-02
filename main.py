from dotenv import load_dotenv
from bot import Bot
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import datetime
from twilio_notif import client

load_dotenv()

read_list_info = []
results = []

try:
    with Bot(teardown=False) as bot:
        bot.anime_planet_home_page()
        read_list_info = bot.get_reading_list()[:5]
        bot.reading_site_home_page()
        for info in read_list_info:
            bot.search_title(info["title"])
            link = bot.get_title_page(info["alt_titles"])
            chapter_result = bot.get_latest_chapter(link, info["chapters_read"])
            chapter_result["title"] = info["title"]
            print(chapter_result)
            results.append(chapter_result)

except Exception as e:
    if 'in PATH' in str(e):
        print("There is a problem running this program from CLI.")
    else:
        raise

with open('readminder.html', 'r') as f:
    now = datetime.datetime.now()
    email_content = f.read()

    placeholder_title = "Book_Title"
    placeholder_latest_chapter = "Latest_Chapter"
    placeholder_book_summary = "Book_Description"
    placeholder_image = "book.png"
    placeholder_read_link = "#booklink"
    insert_titles = '<!-- Title Entries -->'
    append_from = email_content.index(insert_titles) + len(insert_titles)

    # Populate book info
    for chp_res in results:
        with open('title_entry.html', 'r') as t:
            title_entry = t.read()
            email_content = email_content[:append_from] + title_entry + email_content[append_from:]
            email_content = email_content.replace(
                placeholder_title, chp_res["title"]
            ).replace(
                placeholder_latest_chapter, f'Chapter {chp_res["latest_chapter"]} is out now!'
            ).replace(
                placeholder_book_summary, chp_res["summary"]
            ).replace(
                placeholder_image, chp_res["image"]
            ).replace(placeholder_read_link, chp_res["read_next_chapter"])

    # Send the email
    print('Composing Email...')

    # Email Configuration
    SERVER = 'smtp.gmail.com'
    PORT = 587
    FROM = os.getenv('EMAIL')
    TO = os.getenv('EMAIL')
    PASS = os.getenv('EMAIL_PASS')

    msg = MIMEMultipart()
    msg['Subject'] = 'Readminder [Automated Email] ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
    msg['From'] = FROM
    msg['To'] = TO

    # load and attach images
    fp = open('./images/book-icon.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header('Content-ID', '<logo>')
    msgImage.add_header('Content-Disposition', 'inline', filename='logo')
    msg.attach(msgImage)

    msg.attach(MIMEText(email_content, 'html'))

    print('Initiating Server...')
    server = smtplib.SMTP(SERVER, PORT)
    server.set_debuglevel(1)
    server.ehlo()  # initiate server with "hello"
    server.starttls()  # start secure connection
    server.login(FROM, PASS)
    server.sendmail(FROM, TO, msg.as_string())

    print('Readminder email sent!')

    server.quit()

