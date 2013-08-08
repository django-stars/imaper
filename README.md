# Imaper

IMAP made easy.

**Documentation:** [https://imaper.readthedocs.org/en/latest/](https://imaper.readthedocs.org/en/latest/)

*This library is inspired by [Imbox](https://github.com/martinrusev/imbox).*

## Example

    from imaper import Imaper

    mailbox = Imaper(
        hostname='imap.foo.com',
        username='foo@foo.com',
        password='password'
    )

    print "Messages ({0}/{1})".format(mailbox.unread_count(), mailbox.message_count())
    print "=" * 80

    # Imaper.messages() returns a generator, but I want a list
    messages = list(mailbox.messages(unread=True))

    for msg in messages:
        print "Subject: {0}".format(msg.subject)
        print "Body:\n{0}".format(msg.body['plain'][0])
        print "-" * 80

        # Mark it as read
        msg.mark_read()

    # Delete the first message
    messages[0].delete()


## Install

### Install From PyPi

*Coming soon!* - Once it is tagged for release it will be available.

### Install From Git

Clone the Repository:

    $ git clone https://bitbucket.org/dhrrgn/imaper.git

Install Requirements:

    $ cd imaper
    $ pip install -r requirements.txt


## Local Documentation

Install Fabric if you do not have it install already (`pip install Fabric`).

From the repository's root run:

    $ fab requirements:docs
    $ fab gendocs

The documentation will be located in docs/_build
