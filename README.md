# Barpy for Barpi

Barpy is an open source project built to be run on a Raspberry pi based cocktail robot.

# Overview of the project

https://www.dolthub.com/blog/2021-05-17-dolt-powered-bartender/

# Running Barpy

```
git clone git@github.com:bheni/barpy.git
cd barpy
git-dolt fetch cocktails.git-dolt
git-dolt fetch barpydb.git-dolt
dolt sql-server --config config.yaml
```

connect to the server using the username: "barpy", no password needed

