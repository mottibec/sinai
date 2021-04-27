import time
import logging
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


def get_api_key():
    return "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"


def send_email(max_out):
    sg = sendgrid.SendGridAPIClient(api_key=get_api_key())
    from_email = Email("mybechhofer@gmail.com")
    to_email = To("mybechhofer@gmail.com")
    subject = f"ALERT number of sinai max out has changed to {max_out}"
    content = Content(
        "text/plain",  f"ALERT number of sinai max out has changed to {max_out}")
    mail = Mail(from_email, to_email, subject, content)
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
