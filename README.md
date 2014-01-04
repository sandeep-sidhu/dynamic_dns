dynamic_dns
===========

Update Rackspace Cloud DNS record with your Mac IP address automatically

Usages
===========

./dynamic_dns.py -c <config_file_path>


Setting it to run automcatically in the background
===========

# cd /Users/<username>/Library/LaunchAgents/
# touch com.dynamic_dns.plist


# vi com.dynamic_dns.plist

put following XML in the above plist file ( replace the username/config_file parts )

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC -//Apple Computer//DTD PLIST 1.0//EN http://www.apple.com/DTDs/PropertyList-1.0.dtd >
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>com.dynamic_dns</string>
    <key>Program</key>
    <string>/Users/<username>/dynamic_dns.py -c <config_file></string>
    <key>KeepAlive</key>
    <true/>
  </dict>
</plist>

launchctl load ~/Library/LaunchAgents/com.dynamic_dns.plist

That's it!

Troubleshooting and testing
===========

dynamic_dns.py logs it's logging info to dynamic_dns.log file which you can
configure in the config_file.
Logging Level is also setup in the config_file.


