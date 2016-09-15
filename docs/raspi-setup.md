# Raspberry Pi

Suggested configuration and software for Raspberry Pi 3

## Initial setup

- Download Raspian
- Format SDHC to FAT32
- Install Raspian on SDHC
    - The following is an example for mac os and Linux
    - `sudo dd bs=1m if=~/Downloads/2016-05-27-raspbian-jessie.img of=/dev/rdisk6`
- Connect mouse, keyboard, HDMI, and power to raspi 3

## After boot

- Open Menu->Preferences->Raspberry Pi Configuration
    - Open Interfaces tab
    - Enable Camera, SSH, I2C, and Serial
    - Open Localisation tab
    - Set values for Locale, Timezone, Keyboard, and WiFi Country
    - close and reboot
- Open terminal
    - `sudo apt-get update`
    - `sudo apt-get upgrade`
    - `sudo apt-get install vim`
        - optionally install color schemes like monokai, badwold, and solarized
    - `sudo apt-get install i2c-tools`
    - `sudo apt-get install tmux`
- Setup WiFi
    - Only need if using raspi 3 and if you wish to connect to your wifi
    - Click network icon in menbar (two computer icon at top-right)
    - Select your network
    - Enter your network password
- Setup static IPv4 address
    - see https://www.modmypi.com/blog/how-to-give-your-raspberry-pi-a-static-ip-address-update
    - edit /etc/dhcpcd.conf
        - add `interface eth0\nstatic ip_address=192.168.0.x/24`

## git

- Use the following to generate an SSH key for the raspi. This is needed for pushing to remote git services like GitHub and BitBucket
    - `ssh-keygen -t rsa -b 4096 -C "kevin@kevlindev.com"`
- If you used a passphrase with your SSH key (you should), then run the following. You may want this in your login script
    - `eval "$(ssh-agent -s)"`
    - `ssh-add ~/.ssh/id_rsa`
- You can use an X-based GUI to control git
    - `sudo apt-get install git-gui`
- Be sure to setup your email and name as these are associated with every git commit
    - `git config --global user.email "kevin@kevlindev.com"`
    - `git config --global user.name "Kevin Lindsey"`

## VNC

- Install VNC server and start it on raspi
    - `sudo apt-get install tightvncserver`
    - `tightvncserver`
    - set password
- Connect from Mac
    - cmd-K
    - vnc://pi@192.168.0.1:5901
    - enter password

## Apple File Sharing

- `sudo apt-get install netatalk`
- `sudo /etc/init.d/netatalk stop`
- `sudo vim /etc/netatalk/AppleVolumes.default`
    - Edit last line, if necessary
- `sudo /etc/init.d/netatalk start`


# mac os

Suggested configuration and software for mac os machines

## Serial access from mac os

- [Using a console cable](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-5-using-a-console-cable?view=all)
- Get USB Console Cable #954 from Adafruit
- Install PL2303_MacOSX_1_6_0_20151022 driver
    - http://www.prolific.com.tw/US/ShowProduct.aspx?p_id=229&pcid=41
- Connect cable to raspi
    - IMPORTANT: determine if USB will power or if you'll provide power. The following assumes the raspi will get power from the cable
    ![Cable Wiring](./console_cable_gpio.jpg)
- Connect cable to mac
- Open terminal
- type `screen /dev/cu.usbserial 115200`
    - If you don't see anything, you may need to turn on serial support in the kernel on the raspi. See [Initial Setup](#initial-setup)

## X Windows on mac os

- Install XQuartz from https://www.xquartz.org
- Open terminal and shell into raspi
    - `ssh -X pi@192.168.0.1`
- run X app from raspi session
    - for example: `geany &`
    - for example: `idle3 &`
        - You can even run the python scripts for the camera this way but the preview shows on the raspi display, not in X windows
