# dynamic_dns


Update Rackspace Cloud DNS record with your Mac IP address automatically

## Usages

./dynamic_dns.py -c <config_file_path>


## Setting it to run automatically in the background

<pre><code>
# cd /Users/<username>/Library/LaunchAgents/
# touch com.dynamic_dns.plist
# vi com.dynamic_dns.plist
</code></pre>

<p>
put following XML in the above plist file ( replace the username/config_file parts )
</p>


<pre><code>
&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;<br/>&lt;!DOCTYPE plist PUBLIC -//Apple Computer//DTD PLIST 1.0//EN http://www.apple.com/DTDs/PropertyList-1.0.dtd &gt;<br/>&lt;plist version=&quot;1.0&quot;&gt;<br/>  &lt;dict&gt;<br/>    &lt;key&gt;Label&lt;/key&gt;<br/>    &lt;string&gt;com.dynamic_dns&lt;/string&gt;<br/>    &lt;key&gt;Program&lt;/key&gt;<br/>    &lt;string&gt;/Users/&lt;username&gt;/dynamic_dns.py -c &lt;config_file&gt;&lt;/string&gt;<br/>    &lt;key&gt;KeepAlive&lt;/key&gt;<br/>    &lt;true/&gt;<br/>  &lt;/dict&gt;<br/>&lt;/plist&gt;<br/>
</code></pre>

<pre><code>
launchctl load ~/Library/LaunchAgents/com.dynamic_dns.plist
</code></pre>

That's it!

## Troubleshooting and testing
<p>dynamic_dns.py logs it's logging info to dynamic_dns.log file which you can
configure in the config_file.</p>

<p>Logging Level is also setup in the config_file.</p>


