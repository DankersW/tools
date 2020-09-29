# Linux commands and build-in tools

## Commands

### Share ssh keys between Windows and WSL
```sh
sudo umount /mnt/c
sudo mount -t drvfs C: /mnt/c -o metadata
ln -s /mnt/c/Users/<username>/.ssh ~/.ssh
# Add the following to /etc/wsl.conf (remove hashtags)
# [automount]
# options = "metadata"
chmod 600 /mnt/c/Users/<USER>/.ssh/id_rsa
chmod 600 /mnt/c/Users/<USER>/.ssh/id_rsa.pub
```
Followed by changing the permissions on Windows for that file. 
https://superuser.com/questions/1296024/windows-ssh-permissions-for-private-key-are-too-open

### Windows 10 ubuntu bash: mount USB extrernal hard-drive
```sh
sudo mkdir /media/<NAME>
sudo mount -t drvfs D: /media/<NAME>
# un-mount
sudo umount /media/<NAME>
```

## Tools

### WPA_Supplipicant

Wpa_supplicant is a free software implementation of an IEEE 802.11i supplicant for Linux, FreeBSD, NetBSD, QNX, AROS, Microsoft Windows, Solaris, OS/2 and Haiku. In addition to being a fully featured WPA2 supplicant, it also implements WPA and older wireless LAN security protocols

```sh
$: sudo nano /etc/wpa_supplicant/wpa_supplicant.conf 
$: sudo wpa_cli terminate
$: sudo wpa_supplicant -d nl80211 -i wlp1s0 -c etc/wpa_supplicant/wpa_supplicant.conf
```

### TCP dump

Tcpdump is a command-line packets sniffer or package analyzer tool which is used to capture or filter TCP/IP packets that are received or transferred over a network on a specific interface

```sh
tcpdump -i eth0 udp -n
```

 * -i switch only capture from desire interface
 * Add protocol to specifiy protocol (udp/tcp)
 * -n doesn't convert addresses (i.e., host addresses, port numbers, etc.) to names


### NTP

#### Airboard
  
Set the date using an NTP server 
* ntpdate -b 10.42.0.15

#### Server side
* sudo /etc/init.d/ntp start

### MBLMT

Run MBLMT code without installing the libs

```sh
LD_LIBRARY_PATH=/usr/local/lib/mblmt/ MBLMTCore ~/path/file.mod
```

### READ-ONLY File system
On a corrupt file system. Find out which directory is currept then run the following command
```sh
e2fsck -fp /dev/<device>
```
