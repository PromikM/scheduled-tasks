import pandas as pd
from datetime import datetime
import random
import smtplib
import os

# import os and use it to get the Github repository secrets
server = "smtp.gmail.com"
my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("MY_PASSWORD")

df = pd.read_csv("birthdays.csv")

today = datetime.today()
month = today.month
day = today.day

birthday = df[(df["month"] == month) & (df["day"] == day)]


def prepare_letter(data: pd.Series) -> None:
    with open(f"letter_templates/letter_{random.randint(1, 3)}.txt", "r") as f:
        letter = f.read()
        letter = letter.replace("[NAME]", data["name"], 1)

    with smtplib.SMTP(server, 587) as conn:
        conn.starttls()
        conn.login(user=my_email, password=password)
        conn.sendmail(from_addr=my_email, to_addrs=data["email"],
                      msg=f"Subject:Happy Birthday!!\n\n{letter}")


if not birthday.empty:
    for _, row in birthday.iterrows():
        prepare_letter(row)
