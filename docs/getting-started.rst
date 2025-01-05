Getting Started
===============

Installation
------------

.. code-block:: bash

   pip install linkzone

Configuration
-------------

The library uses a configuration file `config.json`:

.. code-block:: json

   {
     "ENDPOINT_URL": "http://192.168.1.1/jrd/webapi",
     "TIMEOUT_REQUESTS": 300,
     "BACKOFF_CONSTANT": 0.1,
     "BACKOFF_EXPONENT_BASE": 1.5
   }

Usage
-----

### Authentication

.. code-block:: python

   from linkzone import Authentication

   # Create authentication instance
   auth = Authentication()

   # Login
   token = auth.login("admin_password")

### Sending SMS

.. code-block:: python

   from linkzone import SMS

   # Create SMS instance
   sms = SMS()

   # Send message
   response = sms.send_sms(
       phone_numbers=["1234567890"], 
       message="Hello world!"
   )