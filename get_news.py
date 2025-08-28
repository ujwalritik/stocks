from Web_Scraping.buisness_line import other_news as blo
from Web_Scraping.buisness_today import other_news as bto
from Web_Scraping.buisness_line_headline import headlines as bl
from Web_Scraping.buisness_today_headline import headlines as bt
import threading

t1 = threading.Thread(target=bt)
t2 = threading.Thread(target=bl)
t3 = threading.Thread(target=blo)
t4 = threading.Thread(target=bto)

t1.start()
t2.start()
t3.start()
t4.start()


