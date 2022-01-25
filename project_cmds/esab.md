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

### Instaling a deb package on the GW

Note: ```The package resides in the currert dirrectoy```

```sh
sudo apt install ./package.deb
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

### gRPC

Building the gRPC files for python
```sh
pip3 install .
pip3 install grpcio-tools
make grpc
```

## Curl
```sh
# Post with data
curl --header "Content-Type: application/json" --request POST --data '{"file_path": "/home/iotgw/edge.ecf"}' 192.168.0.103:8080/api/upgrade

# File upload
curl -F 'file=@test_file.txt' 192.168.0.103:8080/api/upgrade
```
