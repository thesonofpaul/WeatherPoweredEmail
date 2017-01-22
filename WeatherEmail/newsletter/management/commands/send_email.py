from smtplib import SMTPException

from django.core.mail import send_mass_mail
from django.core.management.base import BaseCommand, CommandError
from newsletter.models import EmailList
from urllib.request import urlopen
from json import loads
import datetime
from re import match


def get_email_subject(temp_current, temp_avg, condition):
    condition = condition.lower()
    temp_delta = temp_current-temp_avg
    if temp_delta >= 5 or ('sun' in condition and 'part' not in condition):
        return 'It\'s nice out! Enjoy a discount on us.'
    elif temp_delta <= -5 or match("(rain|sleet|flurries|snow|storm)", condition) is not None:
        return 'Not so nice out? That\'s okay, enjoy a discount on us.'
    else:
        return 'Enjoy a discount on us.'


def get_date_range():
    today = datetime.datetime.now()
    delta = datetime.timedelta(days=15)
    start = (today - delta).strftime("%mm%dd")
    end = (today + delta).strftime("%mm%dd")
    return '{}{}'.format(start, end)


def get_weather(city, state):
    wunderground_url = 'http://api.wunderground.com/api/{}/{}/conditions/q/{}/{}.json'
    my_key = '4207ee15e36205ec'
    dates = 'planner_{}'.format(get_date_range())

    if ' ' in city:
        city = city.replace(' ', '_')

    try:
        f = urlopen(wunderground_url.format(my_key, dates, state, city))
        json_string = f.read()
        parsed_json = loads(json_string)
        condition = parsed_json['current_observation']['weather']
        temp_current = int(parsed_json['current_observation']['temp_f'])
        temp_avg_low = int(parsed_json['trip']['temp_low']['avg']['F'])
        temp_avg_high = int(parsed_json['trip']['temp_high']['avg']['F'])
    except (IOError, TypeError):
        raise CommandError('Error retrieving weather data for {}, {}'.format(city, state))
    else:
        temp_avg = (temp_avg_high + temp_avg_low) / 2
        f.close()
        return temp_current, temp_avg, condition


def compose_email(temp_current, temp_avg, condition, recipient):
    my_email = 'weather.powered.email.test@gmail.com'

    email_subject = get_email_subject(temp_current, temp_avg, condition)
    email_body = '{} degrees, {}'.format(temp_current, condition)
    return email_subject, email_body, my_email, [recipient]


class Command(BaseCommand):

    def handle(self, *args, **options):
        email_list = []
        for item in EmailList.objects.all():
            temp_current, temp_avg, condition = get_weather(item.location.city, item.location.state)
            email_list.append(tuple(compose_email(temp_current, temp_avg, condition, item.email_address)))

        print(len(email_list))
        try:
            send_mass_mail(email_list)
        except SMTPException:
            raise CommandError('Error, emails were not sent correctly.')
