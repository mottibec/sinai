import time
import logging
import os
from pyquery import PyQuery as pq
import sendgrid
from sendgrid.helpers.mail import *


current_max = "600"


def get_max_out():
    logging.info("getting max out")
    page = pq(url="https://borderpay.metropolinet.co.il/order-page")
    taba_option = page("#BoarderName option[value='1061']")
    max_out = taba_option.attr("max-out-for-day")
    logging.info(f"got max_out of {max_out}")
    return max_out


def get_env(key):
    return os.environ.get(key)


def send_email(max_out):
    sg = sendgrid.SendGridAPIClient(api_key=get_env("SENDGRID_API_KEY"))
    from_email = Email(get_env("SENDER_EMAIL"))
    to_email = To(get_env("RECEIVER_EMAIL"))
    text = f"ALERT, the number of sinai max out has changed to {max_out}"
    content = Content("text/plain",  text)
    mail = Mail(from_email, to_email, text, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    logging.info(response.status_code)


def main():
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    max_out = get_max_out()
    while max_out == current_max:
        time.sleep(10)
        max_out = get_max_out()
    send_email(max_out)


main()
