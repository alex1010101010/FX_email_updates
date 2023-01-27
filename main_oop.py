import smtplib
import yfinance as yf
from dotenv import load_dotenv
import os

load_dotenv()

class Fx_Obj:
    def __init__(self):
        self.FX_rates = {"eur_usd": yf.Ticker('EURUSD=X').history(period='30d')['Close'],
                    "gbp_usd": yf.Ticker('GBPUSD=X').history(period='30d')['Close'],
                    "gbp_eur": yf.Ticker('GBPEUR=X').history(period='30d')['Close'],
                    "gbp_aud": yf.Ticker('GBPAUD=X').history(period='30d')['Close']
                    }

        # Daily change
        self.Dailys = {fx: (fx_data[-1]/fx_data[-2]-1)*100 for fx, fx_data in self.FX_rates.items()}

        # Weekly change
        self.Weeklys = {fx: (fx_data[-1]/fx_data[-7]-1)*100 for fx, fx_data in self.FX_rates.items()}


        # Monthly change
        self.Monthlys = {fx: (fx_data[-1]/fx_data[-30]-1)*100 for fx, fx_data in self.FX_rates.items()}


        # FX rates formatted
        self.rounded_FX = {
                    "eur_usd": round(self.FX_rates['eur_usd'][0],2),
                    "gbp_usd": round(self.FX_rates['gbp_usd'][0],2),
                    "gbp_eur": round(self.FX_rates['gbp_eur'][0],2),
                    "gbp_aud": round(self.FX_rates['gbp_aud'][0],2)
        }

    def to_f_statement(self, rate):
        return "{}%".format("%.2f" % rate)

    def send_email(self):
        sent_from = os.getenv('sender')
        to = [os.getenv("receiver")]
        subject = 'Daily FX rates'
        body = f'Current FX rates: EUR to USD {self.FX_rates["eur_usd"][0]}, GBP to USD {self.FX_rates["gbp_usd"][0]}, GBP to EUR {self.FX_rates["gbp_eur"][0]}, GBP to AUD {self.FX_rates["gbp_aud"][0]}' \
                f'\n'\
               f' \n Daily changes: EUR to USD {self.to_f_statement(self.Dailys["eur_usd"])}, GBP to USD {self.to_f_statement(self.Dailys["gbp_usd"])}, GBP to EUR {self.to_f_statement(self.Dailys["gbp_eur"])},' \
               f'GBP to AUD {self.to_f_statement(self.Dailys["gbp_aud"])}' \
                f'\n'\
               f' \n Weekly changes: EUR to USD {self.to_f_statement(self.Weeklys["eur_usd"])}, GBP to USD {self.to_f_statement(self.Weeklys["gbp_usd"])}, GBP to EUR {self.to_f_statement(self.Weeklys["gbp_eur"])},' \
               f' GBP to AUD {self.to_f_statement(self.Weeklys["gbp_aud"])}' \
                f'\n'\
               f' \n Monthly changes: EUR to USD {self.to_f_statement(self.Monthlys["eur_usd"])}, GBP to USD {self.to_f_statement(self.Monthlys["gbp_usd"])}, GBP to EUR {self.to_f_statement(self.Monthlys["gbp_eur"])},' \
               f' GBP to AUD {self.to_f_statement(self.Monthlys["gbp_aud"])}'

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
