# GraphQL server application

This is a GraphQL server which will be used to send the IXP data to a frontend.


## Before running the server

The data are retrieved by a PostgreSQL DB, so you need to setup a DB before run the server.

The server also needs some configuration parameters to run, like the DB credentials. There is a configuration template file, `graphql_srv_config.conf.in`, which can be changed in a configuration file like the following

```
sed "s|@DB_HOST@|localhost|g; \
     s|@DB_PORT@|5432|g; \
     s|@DB_USER@|ixp|g; \
     s|@DB_PASS@|PchL00k1ngGl@ss|g; \
     s|@DB_NAME@|ixp|g;" graphql_srv_config.conf.in > graphql_srv_config.conf
```

The above command will create a configuration file, `graphql_srv_config.conf` with the following contents

```
$ cat graphql_srv_config.conf
db-host = localhost
db-port = 5432
db-user = ixp
db-pass = PchL00k1ngGl@ss
db-name = ixp
```


### Configuration parameters details

The configuration parameters are the following

* db-host: The host of the DB.
* db-port: The port of the DB.
* db-user: The username to connect to the DB.
* db-pass: The password of the user to connect to the DB.
* db-name: The name of the DB to connect.


## Running the server

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
$ python3 src/app.py

```

In order to verify that the server is running, go to a browser and add the link `http://localhost:5000/graphql`. You should see the GraphiQL interface. In order to get all the IXP data, you can add the following query

```
{
  ixps {
    ixp
    ixpCity
    ixpCountry
    ixpIpVersion
    ixpLocalAsn
    ixpRibEntries
    ixpNumberOfPeers
    ixpNumberOfNeighbors
    dateAdded
  }
}
```


## Building the docker image

Executing the following command you can build the docker image

```
docker build -t graphql_srv-image .
```


## Running the docker image

Executing the following command you can run the docker image

```
docker run --net=host \
            -e DB_HOST="127.0.0.1" \
            -e DB_PORT=5432 \
            -e DB_USER="ixp" \
            -e DB_PASS="PchL00k1ngGl@ss" \
            -e DB_NAME="ixp" \
            graphql_srv-image

```

The `--net=host` is used because the DB is located on host.
