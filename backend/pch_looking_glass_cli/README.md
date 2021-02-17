# PCH Looking Glass client

This is a client that retrieves IXP data from the PCH Looking Glass tool which can be found here, `https://www.pch.net/tools/looking_glass/`. The data are stored in a PostgreSQL database.


## Before running the client

The client stores the data in a PostgreSQL DB, so you need to setup a DB before run the client.

The client also needs some configuration parameters to run, like the DB credentials. There is a configuration template file, `pch_looking_glass_cli_config.conf.in`, which can be changed in a configuration file like the following

```
sed "s|@CACHE_DIR@|/tmp|g; \
     s|@DB_HOST@|localhost|g; \
     s|@DB_PORT@|5432|g; \
     s|@DB_USER@|ixp|g; \
     s|@DB_PASS@|PchL00k1ngGl@ss|g; \
     s|@DB_NAME@|ixp|g;" pch_looking_glass_cli_config.conf.in > pch_looking_glass_cli_config.conf
```

The above command will create a configuration file, `pch_looking_glass_cli_config.conf` with the following contents

```
$ cat pch_looking_glass_cli_config.conf
cache-dir = /tmp
db-host = localhost
db-port = 5432
db-user = ixp
db-pass = PchL00k1ngGl@ss
db-name = ixp
```

### Configuration parameters details

The configuration parameters are the following

* cache-dir: The cache directory to store any cached info.
* db-host: The host of the DB.
* db-port: The port of the DB.
* db-user: The username to connect to the DB.
* db-pass: The password of the user to connect to the DB.
* db-name: The name of the DB to connect.


## Running the client

You need to install `pipenv`, in order to install run the following

```
$ pip3 install pipenv
```

Execute the following in order to install the runtime dependencies as described from the `requirements.txt` and `Pipfile` files.

```
$ pipenv install
```

Now in order to run the client you execute the following

```
$ pipenv shell
$ python3 src/pch_looking_glass_cli.py

```


## Building the docker image

Executing the following command you can build the docker image

```
docker build -t pch_looking_glass_cli-image .
```


## Running the docker image

Executing the following command you can run the docker image

```
docker run --net=host \
            -e CACHE_DIR="/tmp" \
            -e DB_HOST="127.0.0.1" \
            -e DB_PORT=5432 \
            -e DB_USER="ixp" \
            -e DB_PASS="PchL00k1ngGl@ss" \
            -e DB_NAME="ixp" \
            pch_looking_glass_cli-image

```

The `--net=host` is used because the DB is located on host.
