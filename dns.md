# DNS is changing from the way we know it

DNS is the phone book of internet, DNS server gives resolution of domain name to IP address used to connect to the server hosting the web site. 

DNS is on port UDP 53 and unencrypted by default, though internet traffic is encrypted with HTTPS, but DNS queries and responses are not encrypted. 

There were two questions - Privacy and Security.

Anyone can eavesdrop and see what you are browsing. It is also used by Internet Service Providers and Organizations for content filtering, blocking known malware, phishing and other unwanted traffic.

DNS-over-tls and DNS-over-https encrypt DNS request and responses. They are great for privacy, but differing views have emerged on security. ISPs and Organizations prefered DNS-over-tls as it is on predefined port of 853, it can still provide some visibility. But DNS-over-https creates blind spot for administrators as it interleaves with other https traffic.

DNS-over-https is prefered by web companies, Mozilla Firefox is providing first class support and Google releasing the feature as experimental to select users with version 83.

On Mozilla Firefox 

Preferences -> Network settings -> settings

image

Cloudflare DNS server is default, but it also gives option for custom server supporting dns-over-https.

On Google Chrome

chrome://flags/#dns-over-https

image 

Chrome will try dns-over-https for ISP DNS server, if it does not support it will fall back to DNS over UDP port 53. 

Browsers become independent of DNS server configured on operating system. 








