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
client.ClientLogin('sprksh.j@gmail.com'.encode(), 'SP.123@tcs'.encode())

# Query the server for an Atom feed containing a list of your documents.
documents_feed = client.GetDocumentListFeed()
# Loop through the feed and extract each document entry.
for document_entry in documents_feed.entry:
  # Display the title of the document on the command line.
  print((document_entry.title.text))









