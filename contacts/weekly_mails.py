from .models import MailSend
from home.weekly_templates import *
from datetime import datetime
from workplace.models import Workplace
import time


'''
send mails that you have listed only x products
send mails that your workplace info is not complete
send mail that you have not listed any connections
send mails that no person has registered from your company
send mails that only one person has registered from your company
send mails that to access basic crm features more people should be listed
send mails that you have not selected cities so you cannot see the network effect
send mail that you have not listed segments your company lies in so you cannot get relevant network
send mail that you can post requirements and get quotations
send mails that you have got n views till now
send mails that you have not posted any updates, through updates you can connect to all SMEs at once
send mails to check out new product listing facility
that product you have added don't have good health

Monday: basic overview
Tuesday: Invite users
Wednesday: Network
Thursday: Workplace dat (Identity)
Friday: List Products
Saturday: CRM
'''


def weekly_send():
    day = datetime.today().weekday()
    workplaces = Workplace.objects.filter(workplace_type__in=['A', 'B'])
    now = datetime.now()
    # multiple templates same day
    if day == 0:
        for wp in workplaces:
            up = wp
            subject = "This Week's Overview of your Company Profile"
            body = Monday_template.format(up, wp, wp.slug, wp.hits, '34')
            text = Monday_template_text.format(up, wp, wp.slug, wp.hits, '34')
            emails = wp.get_emails_free()
            if emails:
                m2 = MailSend.objects.filter(email=emails, body=body, text_content=text, subject=subject,
                                             date=now, reasons='wm')
            users = wp.get_members()
            for up in users:
                subject = "This Week's Overview of your Company Profile"
                body = Monday_template.format(up, wp, wp.slug, wp.hits, '34')
                text = Monday_template_text.format(up, wp, wp.slug, wp.hits, '34')
                m = MailSend.objects.filter(email=up.get_emails(), body=body, text_content=text, subject=subject,
                                            date=now, reasons='wm')

            time.sleep(0.1)
    if day == 1:
        for wp in workplaces:
            up = wp
            subject = 'Bring Your Colleagues to CoreLogs'
            body = Tuesday_template.format(up)
            text = Tuesday_template_text.format(up)
            emails = wp.get_emails_free()
            if emails:
                m2 = MailSend.objects.filter(email=emails, body=body, text_content=text, subject=subject,
                                             date=now, reasons='wm')
            users = wp.get_members()
            for up in users:
                subject = 'Bring Your Colleagues to CoreLogs'
                body = Tuesday_template.format(up)
                text = Tuesday_template_text.format(up)
                m = MailSend.objects.filter(email=up.get_emails(), body=body, text_content=text, subject=subject,
                                            date=now, reasons='wm')
            time.sleep(0.1)
    if day == 2:
        for wp in workplaces:
            up = wp
            subject = 'Join Your Business Network And Expand it.'
            body = Wednesday_template.format(up)
            text = Wednesday_template_text.format(up)
            emails = wp.get_emails_free()
            if emails:
                m2 = MailSend.objects.filter(email=emails, body=body, text_content=text, subject=subject,
                                             date=now, reasons='wm')
            users = wp.get_members()
            for up in users:
                subject = 'Join Your Business Network And Expand it.'
                body = Wednesday_template.format(up)
                text = Wednesday_template_text.format(up)
                m = MailSend.objects.filter(email=up.get_emails(), body=body, text_content=text, subject=subject,
                                            date=now, reasons='wm')
            time.sleep(0.1)

    if day == 3:
        for wp in workplaces:
            up = wp
            subject = 'Your Company Profile and Dashboard - Measure your Reach'
            body = Thursday_template.format(up, wp, wp.slug, wp.get_info_score, wp.get_product_score,
                                            wp.get_tags_score)
            text = Thursday_template_text.format(up, wp, wp.slug, wp.get_info_score, wp.get_product_score,
                                                 wp.get_tags_score)
            emails = wp.get_emails_free()
            if emails:
                m2 = MailSend.objects.filter(email=emails, body=body, text_content=text, subject=subject,
                                             date=now, reasons='wm')
            users = wp.get_members()
            for up in users:
                subject = 'Your Company Profile and Dashboard - Measure your Reach'
                body = Thursday_template.format(up, wp, wp.slug, wp.get_info_score, wp.get_product_score,
                                                wp.get_tags_score)
                text = Thursday_template_text.format(up, wp, wp.slug, wp.get_info_score, wp.get_product_score,
                                                     wp.get_tags_score)
                m = MailSend.objects.filter(email=up.get_emails(), body=body, text_content=text, subject=subject,
                                            date=now, reasons='wm')
            time.sleep(0.1)
    if day == 4:
        for wp in workplaces:
            up = wp
            subject = "List Your Products. That's On You."
            body = Friday_template.format(up, wp.get_product_count())
            text = Friday_template_text.format(up, wp.get_product_count())
            emails = wp.get_emails_free()
            if emails:
                m2 = MailSend.objects.filter(email=emails, body=body, text_content=text, subject=subject,
                                             date=now, reasons='wm')
            users = wp.get_members()
            for up in users:
                subject = "List Your Products. That's On You."
                body = Friday_template.format(up, wp.get_product_count())
                text = Friday_template_text.format(up, wp.get_product_count())
                m = MailSend.objects.filter(email=up.get_emails(), body=body, text_content=text, subject=subject,
                                            date=now, reasons='wm')
            time.sleep(0.1)
    if day == 5:
        for wp in workplaces:
            up = wp
            subject = 'Cloud CRM for your Business. Tell us what features you want'
            body = Saturday_template.format(up)
            text = Saturday_template_text.format(up)
            emails = wp.get_emails_free()
            if emails:
                m2 = MailSend.objects.filter(email=emails, body=body, text_content=text, subject=subject,
                                             date=now, reasons='wm')
            
            users = wp.get_members()
            for up in users:
                subject = 'Cloud CRM for your Business. Tell us what features you want'
                body = Saturday_template.format(up)
                text = Saturday_template_text.format(up)
                m = MailSend.objects.filter(email=up.get_emails(), body=body, text_content=text, subject=subject,
                                            date=now, reasons='wm')
                
    if day == 6:
        pass
    else:
        print('WTF')

