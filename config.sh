#!/bin/bash

#Shell script to configure new server

#Config Variables
HOSTNAME=wittgenstein
FQDN=server.cnmipss.org

#Update-upgrade
apt-get update
apt-get upgrade -y

#Use net-tools to get IPADDR
apt-get install net-tools
IPADDR=$(/sbin/ifconfig eth0 | awk '/inet / { print $2 }' | sed 's/addr://')

echo $HOSTNAME > /etc/hostname
hostname -F /etc/hostname

echo $IPADDR $FQDN $HOSTNAME >> /etc/hosts

#Key packages
apt-get install -y \
        emacs-nox \
        fail2ban \
        sendmail \
        nmap \
        ufw \
        tasksel \
        git \
        nodejs \
        nodejs-legacy \
        npm \
        openjdk-8-jdk \
        


#Configure firewall
ufw default allow outgoing
ufw default deny incomming

ufw allow ssh
ufw allow http/tcp
ufw allow https/tcp




        
