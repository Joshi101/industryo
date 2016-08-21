from .templates import *
from passwords.passwords import *
from django.core.mail import EmailMultiAlternatives, get_connection
import time, random


def ses_send():
    smtp_server = 'email-smtp.us-west-2.amazonaws.com'
    # smtp_username = sprksh_username      # sprksh
    # smtp_password = sprksh_password


    smtp_username = sp_username      # sp
    smtp_password = sp_password
    smtp_port = '587'
    smtp_do_tls = True

    # server = smtplib.SMTP(
    #     host = smtp_server,
    #     port = smtp_port,
    #     timeout = 10
    # )
    # server.set_debuglevel(10)
    # server.starttls()
    # server.ehlo()
    # server.login(smtp_username, smtp_password)
    # server.sendmail(fromaddr, toaddrs, msg)
    # print server.quit()


    subject = 'Overview of CoreLogs & Benefits to SMEs'
    html_content = Template_SME_all

    connection = get_connection(host=smtp_server,
                                port=smtp_port,
                                username=smtp_username,
                                password=smtp_password,
                                use_tls=smtp_do_tls)

    # try:
    connection.open()
    from_email = 'sp@corelogs.com'

    text_content = '''Hi,

Greetings from CoreLogs. You have registered your company on CoreLogs. Let me give you a quick overview of CoreLogs and what benefits SMEs can get from it.

CoreLogs is a business enabling platform for SMEs which brings the buyers and sellers/manufacturers and service providers on the same platform along with their products and requirements and boosts business through free interactions via inquiries, leads, quotations and direct messages.

It has 3 basic components:

1. Uniform identity to all SMEs on Internet: CoreLogs gives free and uniform company profile to all SMEs big or small across segments. The company profile will serve as SMEs' identity on internet the way facebook/ linkedin profile is for individuals. We have thousands of SMEs registered and we are expanding fast with an aim to bring all SMEs on one platform.
2. The Business Oriented Network: Bringing all SMEs on one Platform and letting them interact for all business purposes via leads, inquiries, messages and quotations we have created a network of SMEs. Here we bring you together with SMEs of your segment, your city/ Industrial areas and companies of your concern. Companies can always share updates with the entire network at one place.
3. Basic CRM tools & Analytics: On CoreLogs, you list all products/ services and Requirements and get inquiries, quotations and messages from SMEs directly. You can easily manage all of these at one place and thus we help you in getting new customers as well as a basic customer relationship management services. And on company dashboard, we bring you basic analytics data about your company.

Combining all these, we are becoming a one stop platform for small, medium and large businesses. And we are working very hard to create an open platform for SMEs and it is incomplete without you people. Also, to expand the network fast, we ask you to invite more SMEs to CoreLogs. Sooner or later every business is going to be on CoreLogs. More SMEs from your network on CoreLogs brings yo in center and helps you get more business.

If you registered on CoreLogs more than 20 days ago, you need to visit it again and update your profile. We have added features and made the flow easier. And yes the platform is getting bigger everyday.

Any Queries? Mail us at sp@corelogs.com or reply to this email.

Thanks
Surya Prakash
Founder, CoreLogs
                    '''
    msg = EmailMultiAlternatives(subject, text_content, from_email, ['rohit9gag@gmail.com'], connection=connection)
    msg.attach_alternative(html_content, "text/html")
    # msg.send()
    print('SEnd hone se pehle takaaya')
    msg.send()

    # except Exception:
    #     print('Connection hi nahi hua')