Imaper
==========

Version: **1.0.0**

This package allows you to easily access any IMAP mailbox with just a few lines of code.

**Bitbucket Repo:** https://bitbucket.org/dhrrgn/imaper

.. code-block:: python

    from imaper import Imaper

    mailbox = Imaper(
        hostname='imap.foo.com',
        username='foo@foo.com',
        password='password'
    )

    print "Messages ({0}/{1})".format(mailbox.unread_count(),
        mailbox.message_count())
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


:mod:`imaper` Package
==============

.. automodule:: imaper
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`parser` Module
--------------------

.. automodule:: imaper.parser
    :members:
    :undoc-members:
    :show-inheritance:
