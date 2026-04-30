PostgreSQL setup, fixtures, search, and feed
============================================

Install dependencies
--------------------

.. code-block:: powershell

   python -m pip install -r requirements.in

Start the full application stack with Docker:

.. code-block:: powershell

   docker compose up --build

The ``web`` service runs Django on http://localhost:8000. The ``db`` service
creates the ``college_blog`` database and the ``college_blog_user`` role with
the default settings used by Django. Migrations run automatically when the web
container starts.

Run management commands through the Django container:

.. code-block:: powershell

   docker compose run --rm web python manage.py loaddata sample_blog_data
   docker compose run --rm web python manage.py test

If you install PostgreSQL directly instead, create the database and user:

.. code-block:: sql

   CREATE DATABASE college_blog;
   CREATE USER college_blog_user WITH PASSWORD 'college_blog_password';
   ALTER ROLE college_blog_user SET client_encoding TO 'utf8';
   ALTER ROLE college_blog_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE college_blog_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE college_blog TO college_blog_user;

The project reads these optional environment variables:

.. code-block:: powershell

   $env:POSTGRES_DB = "college_blog"
   $env:POSTGRES_USER = "college_blog_user"
   $env:POSTGRES_PASSWORD = "college_blog_password"
   $env:POSTGRES_HOST = "localhost"
   $env:POSTGRES_PORT = "5432"

For a quick SQLite-only local run, set ``USE_SQLITE=1``.

Local Python fallback
---------------------

If you are not using the Docker web container, install dependencies locally:

.. code-block:: powershell

   python -m pip install -r requirements.in

Then migrate and load data:

.. code-block:: powershell

   python manage.py migrate
   python manage.py loaddata sample_blog_data

To export current blog data to a fixture:

.. code-block:: powershell

   python manage.py dumpdata auth.User blog.Post blog.Comment taggit --indent 2 --output blog/fixtures/blog_data.json

To import that exported data later:

.. code-block:: powershell

   python manage.py loaddata blog_data

Feature URLs
------------

- Blog search: ``/search/``
- RSS feed: ``/feed/``
- Sitemap: ``/sitemap.xml``
