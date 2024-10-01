sudo apt install default-jre


sudo groupadd tomcat
sudo useradd -s /bin/false -g tomcat -d /opt/tomcat tomcat

# We will install Tomcat to the /opt/tomcat directory. 
# Create the directory, then extract the archive to it with these commands:
#wget http://www-us.apache.org/dist/tomcat/tomcat-9/v9.0.29/bin/apache-tomcat-9.0.29.tar.gz
wget https://archive.apache.org/dist/tomcat/tomcat-9/v9.0.63/bin/apache-tomcat-9.0.63.tar.gz
sudo mkdir /opt/tomcat
sudo tar xzvf apache-tomcat-9.0.63.tar.gz -C /opt/tomcat --strip-components=1

# Give the tomcat group ownership over the entire installation directory:
sudo chgrp -R tomcat /opt/tomcat
sudo chown -R tomcat webapps/ work/ temp/ logs/

# Get JAVA_HOME
sudo update-java-alternatives -l
java-1.11.0-openjdk-amd64      1111       /usr/lib/jvm/java-1.11.0-openjdk-amd64
export JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64

sudo nano /etc/systemd/system/tomcat.service
# sudo nano /lib/systemd/system/tomcat.service  #

"""
[Unit]
Description=Apache Tomcat Web Application Container
After=network.target

[Service]
Type=forking

Environment=JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64
Environment=CATALINA_HOME=/opt/tomcat
Environment=CATALINA_BASE=/opt/tomcat
Environment='CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC'
Environment='JAVA_OPTS=-Djava.awt.headless=true -Djava.security.egd=file:/dev/./urandom'

ExecStart=/opt/tomcat/bin/startup.sh
ExecStop=/opt/tomcat/bin/shutdown.sh

User=tomcat
Group=tomcat
UMask=0007
RestartSec=10
Restart=always

[Install]
WantedBy=multi-user.target
"""


## Next, reload the systemd daemon so that it knows about our service file:
sudo systemctl daemon-reload

## Start the Tomcat service by typing:
sudo systemctl start tomcat

## Double check that it started without errors by typing:
sudo systemctl status tomcat

## Tomcat uses port 8080 to accept conventional requests. Allow traffic to that port by typing:
sudo ufw allow 8080

## If you were able to successfully accessed Tomcat,
## now is a good time to enable the service file so that Tomcat automatically starts at boot:
sudo systemctl enable tomcat

 sudo /opt/tomcat/bin/startup.sh


 ## Install GEOSERVER
wget https://sourceforge.net/projects/geoserver/files/GeoServer/2.16.1/geoserver-2.16.1-war.zip
https://sourceforge.net/projects/geoserver/files/latest/download
wget  https://sourceforge.net/projects/geoserver/files/GeoServer/2.20.4/geoserver-2.20.4-war.zip


mkdir geoserver
unzip geoserver-2.20.4-war.zip -d ./geoserver
sudo mv geoserver/geoserver.war /opt/tomcat/webapps/

netsh interface portproxy add v4tov4 listenport=3000 listenaddress=0.0.0.0 connectport=3000 connectaddress=172.18.85.36


netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=8080 connectaddress=172.18.85.36

netsh interface portproxy add v4tov4 listenport=8443 listenaddress=0.0.0.0 connectport=8443 connectaddress=172.18.85.43



keytool -genkey -alias tomcatgeoserver -keyalg RSA
password marciogeoserver
 CN=Marcio Yamashita, OU=Fugro, O=Fugro, L=Houston, ST=Houston, C=US correct
