# Site-Update-Notifier

A bot that stores sites to track in a database, routinely scans the tracked sites for updates, and pushes a notification to the set webhook if an update exists.

## Usage

Make sure Python 2.7 is installed.

### MongoDB Setup

Create a MongoDB Atlas database. Note down your Mongo URI, Cluster name, and Collection name.

### Running the bot

Run setup script:

```
$ chmod +x setup.sh
$ sudo ./setup.sh
```

Update the `config.py` file in `site_update_notifier` with your Mongo URI, Cluster name, and Collection name.

Start the virtual environment:

```
$ source venv/bin/activate
```

Run backend:

```
$ python manage.py runserver --noreload
```

Run the frontend:

```
$ cd frontend
$ npm run start
```
