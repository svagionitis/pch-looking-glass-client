Tasks
======

1. Build a client program to retrieve monitoring data (IP + IPV6 bgp summaries) from an IXP route server using PCH’s publicly available looking glasses `https://www.pch.net/tools/looking_glass/`. Your client should be configurable with:
    1. IXP
    2. City
    3. Country
    4. IP version (4 or 6)

2. Build a parser that can parse the raw summaries and extract the following:
    1. Route Server local ASN
    2. Number of RIB entries
    3. Number of Peers
    4. Total number of neighbors

3. Build a script that periodically (every 5 minutes):

    1. Calls the client of objective (1.) for all available IXP route servers (to avoid rate-limit issues, pause for a few seconds before proceeding to the next RS in the list)
    2. Parses this information
    3. Stores it persistently in a DB table with info (key = (IXP, City, Country)):
        1. IXP
        2. City
        3. Country
        4. RS local ASN
        5. Number of RIB entries
        6. Number of Peers
        7. Total number of neighbors

4. Show any DB changes asynchronously (no polling) in a UI. The UI can be basic (e.g., a simple datatable). However the table should be updated asynchronously when a row is updated (with altered data) in the DB.

5. You can use any technology you like. Suggested technologies:
    1. Python for client, parser and periodic script
    2. PostgreSQL for DB
    3. GraphQL for DB-UI communication (websockets)
    4. HTML/Javascript (datatable) for UI


Bonus requirement: employ docker and docker-compose to build and deploy distinct microservices and package this project.

Resources:
- Python3: https://www.tutorialspoint.com/python3/index.htm
- PostgreSQL: https://www.postgresql.org/docs/
- GraphQL: https://graphql.org/
- Datatables: https://datatables.net/
- Docker: https://www.docker.com/
- Docker-compose: https://docs.docker.com/compose/
- Official ARTEMIS Github repo: https://github.com/FORTH-ICS-INSPIRE/artemis

