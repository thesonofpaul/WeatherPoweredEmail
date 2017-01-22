from smtplib import SMTPException

from django.core.mail import EmailMultiAlternatives, get_connection
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import get_template
from newsletter.models import EmailList
from urllib.request import urlopen
import json
import datetime
from re import match


def get_condition(temp_current, temp_avg, condition):
    condition = condition.lower()
    temp_delta = temp_current - temp_avg
    # assuming that any precipitation means bad weather, check those first
    if temp_delta <= -5 or match("(rain|sleet|flurries|snow|storm|drizzle)", condition) is not None:
        return False
    elif temp_delta >= 5 or ('sun' in condition and 'part' not in condition):
        return True
    else:
        return None


def get_date_range():
    today = datetime.datetime.now()
    delta = datetime.timedelta(days=15)
    start = (today - delta).strftime("%m%d")
    end = (today + delta).strftime("%m%d")
    return '{}{}'.format(start, end)


def get_weather(city, state):
    wunderground_url = 'http://api.wunderground.com/api/{}/{}/conditions/q/{}/{}.json'
    my_key = '4207ee15e36205ec'
    dates = 'planner_{}'.format(get_date_range())

    if ' ' in city:
        city = city.replace(' ', '_')
    if '.' in city:
        city = city.replace('.', '')

    try:
        f = urlopen(wunderground_url.format(my_key, dates, state, city))
        json_string = f.read().decode('utf-8')
        parsed_json = json.loads(json_string)
        condition = parsed_json['current_observation']['weather']
        temp_current = int(parsed_json['current_observation']['temp_f'])
        temp_avg_low = int(parsed_json['trip']['temp_low']['avg']['F'])
        temp_avg_high = int(parsed_json['trip']['temp_high']['avg']['F'])
    except (IOError, TypeError, KeyError):
        raise CommandError('Error retrieving weather data for {}, {}'.format(city, state))
    else:
        temp_avg = (temp_avg_high + temp_avg_low) / 2
        f.close()
        return temp_current, temp_avg, condition


def compose_email(city, state, temp_current, temp_avg, condition, recipient):
    sender_address = 'weather.powered.email.test@gmail.com'
    email_template = get_template('newsletter/email.html')

    is_nice = get_condition(temp_current, temp_avg, condition)

    if is_nice is None:
        email_subject = 'Enjoy a discount on us.'
        icon_src = 'https://icons.wxug.com/i/c/i/clear.gif'
    elif is_nice is True:
        email_subject = 'It\'s nice out! Enjoy a discount on us.'
        icon_src = 'https://icons.wxug.com/i/c/i/clear.gif'
    else:
        email_subject = 'Not so nice out? That\'s okay, enjoy a discount on us.'
        icon_src = 'https://icons.wxug.com/i/c/i/chancerain.gif'

    html_format = {'city': city,
                   'state': state,
                   'date': datetime.date.today().strftime('%b %d, %Y'),
                   'temp_current': temp_current,
                   'condition': condition,
                   'icon_src': icon_src}
    email_body = email_template.render(html_format)
    msg = EmailMultiAlternatives(email_subject, '', sender_address, [recipient])
    msg.attach_alternative(email_body, "text/html")
    return msg


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            connection = get_connection()
            connection.open()
            for item in EmailList.objects.all():
                city = item.location.city
                state = item.location.state
                temp_current, temp_avg, condition = get_weather(city, state)
                msg = compose_email(city, state, temp_current, temp_avg, condition, item.email_address)
                msg.send()
            connection.close()

        except SMTPException:
            raise CommandError('Error, emails were not sent correctly.')
