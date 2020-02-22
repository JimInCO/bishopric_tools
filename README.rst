Bishopric Django Tools
======================

A set of tools to automate some of the common Bishopric tasks. Currently focused on organizing talks.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT


Getting Started
---------------
Setting Up Development Environment
----------------------------------

Make sure to have the following on your host:

* Python 3.6, 3.7 or 3.8
* PostgreSQL_.

First things first.

#. Create a virtualenv: ::

    $ python3.7 -m venv .venv
    > python -m venv .venv

#. Activate the virtualenv you have just created: ::

    $ source .venv/bin/activate
    > .venv\Scripts\activate

     .. note::

        Linux commands have a "$" as a pre-fix
        Windows commands have a ">" as a pre-fix

#. Install development requirements: ::

    $ pip install -r requirements/local.txt
    $ pre-commit install

     .. note::

        the `pre-commit` exists in the generated project as default.
        for the details of `pre-commit`, follow the [site of pre-commit](https://pre-commit.com/).

#. Create a new PostgreSQL database using createdb_ or pgAdmin4: ::

    $ createdb bishopric_tools -U postgres --password <password>

   .. note::

       if this is the first time a database is created on your machine you might need an
       `initial PostgreSQL set up`_ to allow local connections & set a password for
       the ``postgres`` user. The `postgres documentation`_ explains the syntax of the config file
       that you need to change.


#. Set the environment variables for your database(s): ::

    $ export DATABASE_URL=postgres://postgres:<password>@127.0.0.1:5432/bishopric_tools
    > set DATABASE_URL=postgres://postgres:<password>@127.0.0.1:5432/bishopric_tools


.. _PostgreSQL: https://www.postgresql.org/download/
.. _createdb: https://www.postgresql.org/docs/current/static/app-createdb.html
.. _initial PostgreSQL set up: http://suite.opengeo.org/docs/latest/dataadmin/pgGettingStarted/firstconnect.html
.. _postgres documentation: https://www.postgresql.org/docs/current/static/auth-pg-hba-conf.html
.. _direnv: https://direnv.net/

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form.
  Once you submit it, you'll see a "Verify Your E-mail Address" page.
  Go to your console to see a simulated email verification message.
  Copy the link into your browser.
  Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy bishopric_tools

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See the documentation on the cookiecutter-django page `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html





Deployment
----------

The following details how to deploy this application.




Custom Bootstrap Compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The generated CSS is set up with automatic Bootstrap recompilation with variables of your choice.
Bootstrap v4 is installed using npm and customised by tweaking your variables in ``static/sass/custom_bootstrap_vars``.

You can find a list of available variables `in the bootstrap source`_, or get explanations on them in the `Bootstrap docs`_.


Bootstrap's javascript as well as its dependencies is concatenated into a single file: ``static/js/vendors.js``.


.. _in the bootstrap source: https://github.com/twbs/bootstrap/blob/v4-dev/scss/_variables.scss
.. _Bootstrap docs: https://getbootstrap.com/docs/4.1/getting-started/theming/


