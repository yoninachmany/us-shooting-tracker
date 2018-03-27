# us-shooting-tracker
Monitoring shootings across the United States, updating daily.

## Setting up

##### Clone the repo

```
$ git clone https://github.com/yoninachmany/us-shooting-tracker.git
$ cd us-shooting-tracker
```

##### Initialize a virtualenv

```
$ pip install virtualenv
$ virtualenv -p /path/to/python3.x/installation env
$ source env/bin/activate
```

For mac users it will most likely be
```
$ pip install virtualenv
$ virtualenv -p python3 env
$ source env/bin/activate
```
Note: if you are using a python2.x version, point the -p value towards your python2.x path

##### (If you're on a mac) Make sure xcode tools are installed

```
$ xcode-select --install
```

##### Install the dependencies

```
$ pip install -r requirements.txt
```

##### Run the application

```
$ export FLASK_APP=app.py
$ flask run
```

##### Debug mode

```
$ export FLASK_DEBUG=1
$ flask run
```
