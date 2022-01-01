from dotenv import load_dotenv
from bot import Bot
from reading_site import ReadingSite
load_dotenv()

read_list_info = []

try:
    with Bot(teardown=False) as bot:
        # bot.anime_planet_home_page()
        # read_list_info = bot.get_reading_list()
        read_list_info = [{'title': 'Adonis', 'chapters_read': '', 'alt_titles': ['Reminiscence Adonis']}, {'title': 'As You Like It, Margrave', 'chapters_read': '50', 'alt_titles': ['Tteutdaero Haseyo']}]
        bot.reading_site_home_page()
        for info in read_list_info:
            bot.search_title(info["title"])
            bot.get_title_page(info["alt_titles"])
            break
except Exception as e:
    if 'in PATH' in str(e):
        print("There is a problem running this program from CLI.")
    else:
        raise


