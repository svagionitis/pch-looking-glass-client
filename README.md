Tasks
======

a. Build a client program to retrieve monitoring data (IP + IPV6 bgp summaries) from an IXP route server using PCH’s publicly available looking glasses https://www.pch.net/tools/looking_glass/ . Your client should be configurable with:
    i.      IXP
    ii.     City
    iii.    Country
    iv.     IP version (4 or 6)

b. Build a parser that can parse the raw summaries and extract the following:
    i. Route Server local ASN
    ii. Number of RIB entries
    iii. Number of Peers
    iv. Total number of neighbors

c. Build a script that periodically (every 5 minutes):

    i. Calls the client of objective (a) for all available IXP route servers (to avoid rate-limit issues, pause for a few seconds before proceeding to the next RS in the list)

    ii. Parses this information

    iii. Stores it persistently in a DB table with info (key = (IXP, City, Country)):
        1. IXP
        2. City
        3. Country
        4. RS local ASN
        5. Number of RIB entries
        6. Number of Peers
        7. Total number of neighbors

d. Show any DB changes asynchronously (no polling) in a UI. The UI can be basic (e.g., a simple datatable). However the table should be updated asynchronously when a row is updated (with altered data) in the DB.

e. You can use any technology you like. Suggested technologies:
    i. Python for client, parser and periodic script
    ii. PostgreSQL for DB
    iii. GraphQL for DB-UI communication (websockets)
    iv. HTML/Javascript (datatable) for UI


Bonus requirement: employ docker and docker-compose to build and deploy distinct microservices and package this project.

Resources:
    # Python3: https://www.tutorialspoint.com/python3/index.htm
    # PostgreSQL: https://www.postgresql.org/docs/
    # GraphQL: https://graphql.org/
    # Datatables: https://datatables.net/
    # Docker: https://www.docker.com/
    # Docker-compose: https://docs.docker.com/compose/
    # Official ARTEMIS Github repo: https://github.com/FORTH-ICS-INSPIRE/artemis

