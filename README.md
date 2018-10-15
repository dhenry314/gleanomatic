# gleanomatic with RSEngine to write to and read from ResourceSync endpoints.


# Start up
With docker already installed and set up for your system, navigate to the directory and run
```
docker build -t gleanomatic_core .
```
Then run this
```
  ./gleanomatic.sh start
```

## Named volume backup

If you have a volume named 'gleanomatic_rs-static', you could create a backup with this:

docker run -v gleanomatic_rs-static:/volume -v /tmp:/backup --rm loomchild/volume-backup backup rs-static_archive 
