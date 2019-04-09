# Linux commands and build-in tools

## Commands

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

