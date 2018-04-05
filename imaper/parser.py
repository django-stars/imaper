"""
This module is a modified version of the parser from Imbox located here:
https://github.com/martinrusev/imbox

Modified: Dan Horrigan

The MIT License (MIT)

Copyright (c) 2013 Martin Rusev

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from io import StringIO, BytesIO
import base64
import email
from email.header import decode_header
import chardet

__all__ = ['parse_email']


def _decode_mail_header(value, default_charset='us-ascii'):
    """Decode a header value into a unicode string."""
    try:
        headers = decode_header(value)
    except email.errors.HeaderParseError:
        return value.encode(default_charset, 'replace').decode(default_charset)
    else:
        for index, (text, charset) in enumerate(headers):
            try:
                headers[index] = text
            except LookupError:
                # if the charset is unknown, force default
                headers[index] = text.decode(default_charset, 'replace')

        def decode_bytes(header):
            if type(header) is bytes:
                encoding = chardet.detect(header)['encoding']
                return header.decode(encoding)
            return header
        return ''.join(map(decode_bytes, headers))


def _get_mail_addresses(message, header_name):
    """Retrieve all email addresses from one message header."""
    addresses = email.utils.getaddresses(
        header for header in message.get_all(header_name, [])
    )

    for index, (address_name, address_email) in enumerate(addresses):
        addresses[index] = {
            'name': _decode_mail_header(address_name),
            'email': address_email
        }

    return addresses


def _parse_attachment(message_part):
    content_disposition = message_part.get("Content-Disposition", None)

    if content_disposition is None:
        return None

    dispositions = content_disposition.strip().split(";")

    if dispositions[0].lower() == "attachment":
        file_data = message_part.get_payload(decode=True)
        attachment = {
            'content-type': message_part.get_content_type(),
            'size': len(file_data),
            'content': BytesIO(file_data)
        }
        for param in dispositions[1:]:
            params = param.split("=", 1)
            name = params[0]
            value = params[1]
            name = name.lower()

            if 'file' in name:
                filename = message_part.get_filename()
                if decode_header(filename)[0][1] is not None:
                    value = decode_header(filename)[0][0].decode(decode_header(filename)[0][1])
                attachment['filename'] = value

            if 'create-date' in name:
                attachment['create-date'] = value

        if not attachment.get('filename') and message_part.get_filename():
            filename = message_part.get_filename()
            if filename.lower().startswith('=?utf-8?'): # I hate microsoft
                decoded_filename = base64.b64decode(filename[10:]).decode()
                attachment['filename'] = decoded_filename

        return attachment


def parse_email(raw_email):
    email_message = email.message_from_string(raw_email)
    maintype = email_message.get_content_maintype()
    parsed_email = {}

    body = {
        "plain": [],
        "html": []
    }
    attachments = []

    if maintype == 'multipart':
        for part in email_message.walk():
            content = part.get_payload(decode=True)
            content_type = part.get_content_type()
            content_disposition = part.get('Content-Disposition', None)

            if content_type == "text/plain" and content_disposition is None:
                body['plain'].append(content)
            elif content_type == "text/html" and content_disposition is None:
                body['html'].append(content)
            elif content_disposition:
                attachments.append(_parse_attachment(part))

    elif maintype == 'text':
        body['plain'].append(email_message.get_payload(decode=True))

    if len(attachments) > 0:
        parsed_email['attachments'] = attachments

    parsed_email['body'] = body
    email_dict = dict(email_message.items())

    parsed_email['sent_from'] = _get_mail_addresses(email_message, 'from')
    parsed_email['sent_to'] = _get_mail_addresses(email_message, 'to')

    value_headers_keys = ['Subject', 'Date', 'Message-ID']
    key_value_header_keys = ['Received-SPF',
                             'MIME-Version',
                             'X-Spam-Status',
                             'X-Spam-Score',
                             'Content-Type']

    parsed_email['headers'] = []
    for key, value in email_dict.items():
        if key in value_headers_keys:
            valid_key_name = key.lower()
            parsed_email[valid_key_name] = _decode_mail_header(value)

        if key in key_value_header_keys:
            parsed_email['headers'].append({'Name': key,
                                            'Value': value})

    return parsed_email
