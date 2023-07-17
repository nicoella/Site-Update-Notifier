# Site-Update-Notifier

## Usage

Make sure Python 3 is installed.

### MongoDB Setup

Create a MongoDB Atlas database.

Create a `config.py` file in `site_update_notifier` with the following format:

```
config = {
    "MONGO_URI":"[your_mongo_URI]"
}
```

Update `db` and `collection` in`views.py` with the following format:

```
db = mongo_client["[your_cluster_name]"] # Update with your Cluster name

collection = db["[your_collection_name]"] # Update with your Collection name
```

### Running the bot

Run setup script (first time):

```
$ chmod +x setup.sh
$ ./setup.sh
```

Run run script:

```
$ chmod +x run.sh
$ ./run.sh
```
