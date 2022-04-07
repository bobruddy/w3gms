# Files for building docker image to parse schedules from w3gms repeater site

## I use the following command to build this image
This assumes you are located in the directory of the Dockerfile
```
docker build -t w3gms_sched .
```

## I put the following cron entry into crontab to run the parser

```
*/5 * * * * docker run -v /data/w3gms/htdocs/:/working/htdocs/ --rm w3gms_sched > /tmp/out.txt
```
