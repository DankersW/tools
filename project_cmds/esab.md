# Commands used in ESAB

## On gateway

### Get root access

```sh
sudo -i
```

### Update python package on GW

Package reside under ```usr/lib/python3/dist-packages/```.

```sh
scp -r PACKAGE root@IP:usr/lib/python3/dist-packages/
```
