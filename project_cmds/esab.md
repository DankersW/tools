# Commands used in ESAB

## On gateway

### Get root access

```sh
sudo -i
```

### Update python package on GW

Package reside under ```usr/lib/python3/dist-packages/```.

```sh
scp -r PACKAGE root@IP:/usr/lib/python3/dist-packages/
```

### SSH allow root login

```sh
sudo -i
passwd
# type in a password

vi /etc/ssh/sshd_config
echo "change |PermitRootLogin yes| "

systemctl restart ssh
```
