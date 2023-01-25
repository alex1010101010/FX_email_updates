import smtplib
import yfinance as yf
from dotenv import load_dotenv
import os

load_dotenv()

eur_usd = yf.Ticker('EURUSD=X').history(period='30d')['Close']
gbp_usd = yf.Ticker('GBPUSD=X').history(period='30d')['Close']
gbp_eur = yf.Ticker('GBPEUR=X').history(period='30d')['Close']
gbp_aud = yf.Ticker('GBPAUD=X').history(period='30d')['Close']

# Daily change
eur_usd_daily = (eur_usd[-1]/eur_usd[-2]-1)*100

gbp_usd_daily = (gbp_usd[-1]/gbp_usd[-2]-1)*100

gbp_eur_daily = (gbp_eur[-1]/gbp_eur[-2]-1)*100

gbp_aud_daily = (gbp_aud[-1]/gbp_aud[-2]-1)*100


# Weekly change
eur_usd_weekly = (eur_usd[-1]/eur_usd[-7]-1)*100

gbp_usd_weekly = (gbp_usd[-1]/gbp_usd[-7]-1)*100

gbp_eur_weekly = (gbp_eur[-1]/gbp_eur[-7]-1)*100

gbp_aud_weekly = (gbp_aud[-1]/gbp_aud[-7]-1)*100

# Monthly change
eur_usd_monthly = (eur_usd[-1]/eur_usd[-30]-1)*100

gbp_usd_monthly = (gbp_usd[-1]/gbp_usd[-30]-1)*100

gbp_eur_monthly = (gbp_eur[-1]/gbp_eur[-30]-1)*100

gbp_aud_monthly = (gbp_aud[-1]/gbp_aud[-30]-1)*100


# FX rates formatted
eur_usd = round(eur_usd[0],2)
gbp_usd = round(gbp_usd[0],2)
gbp_eur = round(gbp_eur[0],2)
gbp_aud = round(gbp_aud[0],2)

eur_usd_daily_f = "{}%".format("%.2f" % eur_usd_daily)
gbp_usd_daily_f = "{}%".format("%.2f" % gbp_usd_daily)
gbp_eur_daily_f = "{}%".format("%.2f" % gbp_eur_daily)
gbp_aud_daily_f = "{}%".format("%.2f" % gbp_aud_daily)

eur_usd_weekly_f = "{}%".format("%.2f" % eur_usd_weekly)
gbp_usd_weekly_f = "{}%".format("%.2f" % gbp_usd_weekly)
gbp_eur_weekly_f = "{}%".format("%.2f" % gbp_eur_weekly)
gbp_aud_weekly_f = "{}%".format("%.2f" % gbp_aud_weekly)

eur_usd_monthly_f = "{}%".format("%.2f" % eur_usd_monthly)
gbp_usd_monthly_f = "{}%".format("%.2f" % gbp_usd_monthly)
gbp_eur_monthly_f = "{}%".format("%.2f" % gbp_eur_monthly)
gbp_aud_monthly_f = "{}%".format("%.2f" % gbp_aud_monthly)

sent_from = os.getenv('sender')
to = [os.getenv("receiver")]
subject = 'Daily FX rates'
body = f'Current FX rates: EUR to USD {eur_usd}, GBP to USD {gbp_usd}, GBP to EUR {gbp_eur}, GBP to AUD {gbp_aud}' \
        f'\n'\
       f' \n Daily changes: EUR to USD {eur_usd_daily_f}, GBP to USD {gbp_usd_daily_f}, GBP to EUR {gbp_eur_daily_f},' \
       f'GBP to AUD {gbp_aud_daily_f}' \
        f'\n'\
       f' \n Weekly changes: EUR to USD {eur_usd_weekly_f}, GBP to USD {gbp_usd_weekly_f}, GBP to EUR {gbp_eur_weekly_f},' \
       f' GBP to AUD {gbp_aud_weekly_f}' \
        f'\n'\
       f' \n Monthly changes: EUR to USD {eur_usd_monthly_f}, GBP to USD {gbp_usd_monthly_f}, GBP to EUR {gbp_eur_monthly_f},' \
       f' GBP to AUD {gbp_aud_monthly_f}'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(os.getenv("sender"), os.getenv("password"))
    smtp_server.sendmail(sent_from, to, email_text)
    smtp_server.close()
    print ("Email sent successfully!")
except Exception as ex:
    print ("Something went wrong….",ex)


