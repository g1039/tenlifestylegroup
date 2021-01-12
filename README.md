Ten Lifestyle Group
===================

Inventory Management Systen


Requirements:
-------------

- [python3](https://python.org/downloads/>)
- [virtualenv](https://virtualenv.pypa.io/en/stable/>)

Getting Started
---------------

1. Clone the repo:

```
$ git clone https://github.com/NtuDev/tenlifestylegroup.git
$ cd tenlifestylegroup
```

2. Setup the VirtualEnv

```
$ virtualenv ve
$ source ve/bin/activate
```

3. Install requirements:

```
$ pip3 install -r requirements.txt
$ pip3 install -r requirements-dev.txt
```

4. Run tests

```
$ python3 manage.py test
```

5. Setup database

```
$ python3 manage.py migrate
$ python3 manage.py
```

6. Start the application

```
$ python3 manage.py runserver
```

You can now access the demo site on http://localhost:8000

Useful links
------------

Csv Upload, Book and Cancel Bokking

```
$ Upload members csv file: http://127.0.0.1:8000/members/upload
$ Upload inventory csv file: http://127.0.0.1:8000/inventory/upload
$ Create booking: http://127.0.0.1:8000/book/
$ Delete booking: http://127.0.0.1:8000/book/cancel/<booking_id>
```

CSV Files
---------

Download CSV files:

```
$ inventory/csv
$ inventory/csv/members
$ inventory/csv/inventory
```
