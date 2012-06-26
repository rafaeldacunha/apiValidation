'''
Created on 26/03/2012

@author: rafael.cunha
'''
import getpass, imaplib, email  
from email.parser import HeaderParser

M = imaplib.IMAP4_SSL("imap.gmail.com", 993)
#M.login(getpass.getuser(), getpass.getpass())
M.login('rafaelcunha74', '')
M.select()
#typ, data = M.search(None, 'FROM','"omniture"')
typ, data = M.search(None, 'SUBJECT','"my test"')

for num in data[0].split():
    print 'num=' + num
    typ, data = M.fetch(num, '(RFC822)')
    
    # obtem headers e seus valores
    header_data = data[0][1]
    parser = HeaderParser()
    msg = parser.parsestr(header_data)
    headers = msg.keys()
    for i in headers:
        print i + '=' + msg.get(i)
    
    # obtem mail body
    email_body = data[0][1]
    mail = email.message_from_string(email_body)

    # Para cada part do email, identifica o content type
    for part in mail.walk():
        c_type = part.get_content_type()
        c_disp = part.get('Content-Disposition')
        print 'Content type=%s Content Disposition=%s' % (c_type, c_disp)
        if c_type == 'image/png' or c_type =='image/gif':
            filename = 'c:\\tmp\\' + part.get_filename();
            fp = open(filename,'wb');
            fp.write(part.get_payload(decode=True))
            fp.close()
M.close()
M.logout()
   
