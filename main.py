import smtplib
import yfinance as yf
from dotenv import load_dotenv
import os

load_dotenv()

FX_rates = {"eur_usd": yf.Ticker('EURUSD=X').history(period='30d')['Close'],
            "gbp_usd": yf.Ticker('GBPUSD=X').history(period='30d')['Close'],
            "gbp_eur": yf.Ticker('GBPEUR=X').history(period='30d')['Close'],
            "gbp_aud": yf.Ticker('GBPAUD=X').history(period='30d')['Close']
            }

# Daily change
Dailys = {fx: (fx_data[-1]/fx_data[-2]-1)*100 for fx, fx_data in FX_rates.items()}

# Weekly change
Weeklys = {fx: (fx_data[-1]/fx_data[-7]-1)*100 for fx, fx_data in FX_rates.items()}


# Monthly change
Monthlys = {fx: (fx_data[-1]/fx_data[-30]-1)*100 for fx, fx_data in FX_rates.items()}


# FX rates formatted
rounded_FX = {
            "eur_usd": round(FX_rates['eur_usd'][0],2),
            "gbp_usd": round(FX_rates['gbp_usd'][0],2),
            "gbp_eur": round(FX_rates['gbp_eur'][0],2),
            "gbp_aud": round(FX_rates['gbp_aud'][0],2)
}

def to_f_statement(rate):
    return "{}%".format("%.2f" % rate)

sent_from = os.getenv('sender')
to = [os.getenv("receiver")]
subject = 'Daily FX rates'
body = f'Current FX rates: EUR to USD {FX_rates["eur_usd"][0]}, GBP to USD {FX_rates["gbp_usd"][0]}, GBP to EUR {FX_rates["gbp_eur"][0]}, GBP to AUD {FX_rates["gbp_aud"][0]}' \
        f'\n'\
       f' \n Daily changes: EUR to USD {to_f_statement(Dailys["eur_usd"])}, GBP to USD {to_f_statement(Dailys["gbp_usd"])}, GBP to EUR {to_f_statement(Dailys["gbp_eur"])},' \
       f'GBP to AUD {to_f_statement(Dailys["gbp_aud"])}' \
        f'\n'\
       f' \n Weekly changes: EUR to USD {to_f_statement(Weeklys["eur_usd"])}, GBP to USD {to_f_statement(Weeklys["gbp_usd"])}, GBP to EUR {to_f_statement(Weeklys["gbp_eur"])},' \
       f' GBP to AUD {to_f_statement(Weeklys["gbp_aud"])}' \
        f'\n'\
       f' \n Monthly changes: EUR to USD {to_f_statement(Monthlys["eur_usd"])}, GBP to USD {to_f_statement(Monthlys["gbp_usd"])}, GBP to EUR {to_f_statement(Monthlys["gbp_eur"])},' \
       f' GBP to AUD {to_f_statement(Monthlys["gbp_aud"])}'

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
