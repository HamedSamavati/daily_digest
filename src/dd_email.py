import datetime
import requests
import dd_content
import smtplib
from email.message import EmailMessage

class DailyDigestEmail:

    def __init__(self):
        self.content = {
        'quote': { 'include': True, 'content': dd_content.get_random_quote()},
        'weather': { 'include': True, 'content': dd_content.get_weather_forecast()},
        'wikipedia': { 'include': True, 'content': dd_content.get_wikipedia_article()} }

        self.recipients = ["hamedsamavaty@gmail.com"]
        self.credentials = {'user': "hamedsamavatipython@gmail.com",
                            'password':"XXXXX"}

    def send_email(self):
        msg = EmailMessage()
        msg['Subject']= f'Daily Digest - {datetime.date.today().strftime("%d %b %Y")}'
        msg['From']= self.credentials['user']
        msg['To']= self.recipients

        msg_body = self.format_message()
        msg.set_content(msg_body['plaintext'])
        msg.add_alternative(msg_body['html'], subtype='html')


        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(user=self.credentials["user"], password=self.credentials["password"])
        connection.send_message(msg)
        connection.close()

    def format_message(self):
        """Generate email body as plaintext and HTML"""
        text = f'*~*~*~ Daily Digest - {datetime.date.today().strftime("%d %b %Y")} ~*~*~*\n\n'
        if self.content['quote']['include'] and self.content['quote']['content']:   # appending the quote of the day
            text += f'*~*~*~ The quote of the day: ~*~*~*\n'
            text += f'{self.content["quote"]["content"]["quote"]} - {self.content["quote"]["content"]["author"]}\n\n'

        if self.content['weather']['include'] and self.content['weather']['content']:  # appending the weather forecast
            text += f"*~*~*~ The weather forecast for {self.content['weather']['content']['city']} - {self.content['weather']['content']['country']} is ~*~*~*\n\n"
            for forecast in self.content['weather']['content']['periods']:
                text += f'{forecast["timestamp"].strftime("%d %b %H%M")} - {forecast["temp"]} \u00B0C | {forecast["description"]}\n'
            text += '\n\n'

        if self.content['wikipedia']['include'] and self.content['wikipedia']['content']:
            text += f'*~*~*~ Daily random learning ~*~*~*\n'
            text += f'{self.content["wikipedia"]["content"]["title"]}\n {self.content["wikipedia"]["content"]["summary"]}\n{self.content["wikipedia"]["content"]["url"]}'

        html = f""" <html>
        <body>
        <center>
        <h1>Daily Digest - {datetime.date.today().strftime("%d %b %Y")}</h1>
        """

        if self.content['quote']['include'] and self.content['quote']['content']:  # appending the quote of the day
            html += f""" <h2> The quote of the day: </h2>
            <i> {self.content["quote"]["content"]["quote"]} </i> - {self.content["quote"]["content"]["author"]}
            """

        if self.content['weather']['include'] and self.content['weather']['content']:  # appending the weather forecast
            html += f""" <h2> The weather forecast for {self.content['weather']['content']['city']} - {self.content['weather']['content']['country']}: </h2> <table>"""
            for forecast in self.content['weather']['content']['periods']:
                html += f""" 
                <tr>
                    <td>
                    {forecast["timestamp"].strftime("%d %b %H%M")}
                    </td>
                    <td>
                    {forecast["temp"]} \u00B0C
                    </td>
                    <td>
                    {forecast["description"]}
                    </td>
                    <td>
                    {forecast["icon"]}
                    </td>
               </tr> """

            html += '</table>\n\n'

        if self.content['wikipedia']['include'] and self.content['wikipedia']['content']:
            html += f"""<h2>Daily random learning: </h2>\n
            <h3><a href="{self.content["wikipedia"]["content"]["url"]}">{self.content["wikipedia"]["content"]["title"]}</h3>
            <table width=800>
                <tr>
                {self.content["wikipedia"]["content"]["summary"]} 
                </tr>
            </table>
            """
        html += """
        </center>
        </body>
        </html>
        """

        return {'plaintext': text, 'html': html}


if __name__ == '__main__':
    print("Tesing generating of the text and html ...")

    email = DailyDigestEmail()
    message = email.format_message()
    print(f"the plaintext is \n{message['plaintext']}")
    print(f"the html is \n{message['html']}")

    with open('../.venv/message.txt', 'w', encoding="utf-8") as file:
        file.write(message["plaintext"])

    with open('../.venv/message.html', 'w', encoding="utf-8") as file:
        file.write(message["html"])

    print("Testing the send_email() ...")
    # dd_email = DailyDigestEmail()
    email.send_email()

