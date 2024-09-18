# almaty

A humble webservice offering ICS url in tabular form

## Usage with Docker

- create the file `/etc/caltab-conf/config.ini`
- start the container

  ```
  docker run --name almaty -p 8000:8000 -v /etc/caltab-conf:/etc/caltab-conf -d wreiner/almaty:v0.2
  ```

## Reverse proxy for apache2

```
<IfModule mod_proxy.c>
    ProxyPreserveHost On
    ProxyPass "/almaty" "http://some.address:8000/"
    ProxyPassReverse "/almaty" "http://some.address:8000/"
</IfModule>
```