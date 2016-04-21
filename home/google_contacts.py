import atom.data
import gdata.data
import gdata.contacts.client
import gdata.contacts.data
import requests
# ...
gd_client = gdata.contacts.client.ContactsClient(source='corelogs-974')
  # Authorize the client.
# ...


def PrintAllContacts(gd_client):
  feed = gd_client.GetContacts()
  for i, entry in enumerate(feed.entry):
    print(('\n%s %s') % (i+1, entry.name.full_name.text))
    if entry.content:
      print(('    %s') % (entry.content.text))
    # Display the primary email address for the contact.
    for email in entry.email:
      if email.primary and email.primary == 'true':
        print(('    %s') % (email.address))
    # Show the contact groups that this contact is a member of.
    for group in entry.group_membership_info:
      print(('    Member of group: %s') % (group.href))
    # Display extended properties.
    for extended_property in entry.extended_property:
      if extended_property.value:
        value = extended_property.value
      else:
        value = extended_property.GetXmlBlob()
      print(('    Extended Property - %s: %s') % (extended_property.name, value))


def GetContacts():
    r = requests.get('https://www.google.com/m8/feeds/contacts/sprksh.j@gmail.com/full')
    print(r)

import gdata.docs.service

# Create a client class which will make HTTP requests with Google Docs server.
client = gdata.docs.service.DocsService()
# Authenticate using your Google Docs email address and password.
client.ClientLogin('sprksh.j@gmail.com', 'SP.123@tcs')

# Query the server for an Atom feed containing a list of your documents.
documents_feed = client.GetDocumentListFeed()
# Loop through the feed and extract each document entry.
for document_entry in documents_feed.entry:
  # Display the title of the document on the command line.
  print((document_entry.title.text))





from django.contrib.auth.models import User
# from django.http import get_host
from django.shortcuts import render_to_response as render
from django.utils.html import escape
import gdata.contacts.service

GOOGLE_CONTACTS_URI = 'http://www.google.com/m8/feeds/'



def get_url_host(request):
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    host = request.build_absolute_uri('/')[:-1]
    return '%s://%s' % (protocol, host)

def get_full_url(request):
    return get_url_host(request) + request.get_full_path()

def get_auth_sub_url(next):
    scope = GOOGLE_CONTACTS_URI
    secure = False
    session = True
    contacts_service = gdata.contacts.service.ContactsService()
    return contacts_service.GenerateAuthSubURL(next, scope, secure, session);

def get_contact_emails(authsub_token):
    contacts_service = gdata.contacts.service.ContactsService()
    contacts_service.auth_token = authsub_token
    contacts_service.UpgradeToSessionToken()
    emails = []
    feed = contacts_service.GetContactsFeed()
    emails.extend(sum([[email.address for email in entry.email] for entry in feed.entry], []))
    next_link = feed.GetNextLink()
    while next_link:
        feed = contacts_service.GetContactsFeed(uri=next_link.href)
        emails.extend(sum([[email.address for email in entry.email] for entry in feed.entry], []))
        next_link = feed.GetNextLink()
    return emails

def import_contacts(request):
    if request.GET.get('token', ''):
        emails = get_contact_emails(request.GET['token'])
        users = User.objects.filter(email__in=emails)
        return render('google_contacts/results.html', {
            'users': users
        })
    else:
        next = get_full_url(request)
        return render('google_contacts/login.html', {
        'auth_sub_url': get_auth_sub_url(next)
        })

import urllib.request as urllib2
# import lxml
from allauth.socialaccount.models import SocialToken

def get_email_google(request):
    social = request.user.social_auth.get(provider='google-oauth2')
    access = SocialToken.objects.get(id=1)
    access_token = access.token
    url = 'https://www.google.com/m8/feeds/contacts/default/full' + '?access_token=' + social.tokens[access_token]
    req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
    contacts = urllib2.urlopen(req).read()
    # contacts_xml = etree.fromstring(contacts)
    # print
    return render(request, 'search/random_text_print.html')

    # contacts_list = []


    # for entry in contacts_xml.findall('{http://www.w3.org/2005/Atom}entry'):
    #     for address in entry.findall('{http://schemas.google.com/g/2005}email'):
    #         email = address.attrib.get('address')
    #         contacts_list.append(email)