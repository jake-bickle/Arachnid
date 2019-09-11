# Arachnid
An OSINT web crawling tool to find data leakage on a target websites using advanced web scraping and parsing technology.

---
![A picture of the user interface in its early stages](/output_early_showcase.png?raw=true)
## What is Arachnid?
(This README is a work in progress and may change as Arachnid recieves and changes features)
Arachnid is a powerful web crawler that has been refined to effectively accomplish two things: aggressively find and index all of the pages of a target domains (and its subdomains) while also searching for "interesting" data on each page as it crawls. A default scan will search for the following:
* Email addresses
* Phone numbers
* Common documents and files
* Social Media Handles

In addition, users can supply their own custom regular expressions, strings, or custom file extensions to scrape as well. Preconfigured scans allow users to quickly begin using the tool, while custom scan allow users to build a highly individual scan that fits their target.

## Arachnid Usage

### Defualt Scan
The default usage for Arachnid is as follows:
```
arachnid https://example.com
```

This will scan using the default configuration which provides the following behavior:
* Scrape for the following information:
  * Emails
  * Phone numbers
  * Social media handles
  * Common documents and file types
* Crawls and indexes all pages on the domain
* Crawl any additional subdomains of example.com that it finds
* Respect the rules on robots.txt within each subdomain
* Uses the default Firefox user agent header
* Uses no delay when crawling unless otherwise specified in robots.txt

### Other Predefined Scan Types
To help make this tool more useful, there are a few other preconfigured scan types that you can make use of.

**Stealth scan**
```
arachnid https://example.com --stealth
```
A stealth scan will use the Google bot user agent, masking the crawler as Google instead of a regular firefox user. It also has a substantial delay between page requests.

**Aggressive Scan**
```
arachnid https://example.com --aggressive
```
An aggressive scan will ignore robots.txt rules and crawl all pages found on it. Aggressive also enables fuzzing for many pages and subdomains, and crawls at the fastest possible speed.

**Page only Scan**
```
arachnid https://example.com --page-only
```
If there is a single web page you'd like to scrape information off of, page-only will not crawl anywhere and only scrape information found at the specified URL.

All predefined scan types are only a base plate of options. You may override any options they provide by supplying your own arguments.

### Custom Scans
Arachnid also allows users very granular control over how they want to scan to run. Here is a sample custom scan:
```
python3 -m arachnid.py https://example.com --aggressive --find docs phone --agent y --delay medium --doc ".psd" --string "John Doe" --regex "^\d{3}\s?\d{3}$" --fuzz --fuzz_subdomains
```
Here is that scan broken down into its parts:
```
    https://example.com           : Required argument, specifies the domain to target
    --aggressive                  : Causes the formerly mentioned aggressive scan
    --find docs phone             : Only scrapes for common documents and phone numbers
    --agent y                     : Uses the Yahoo SearchBot header sting
    --delay medium                : Overrides the timing of the aggressive scan and causes a medium delay, or about 4-11 seconds
    --doc ".psd"                  : In addition to common docs, the crawler will also look for .psd files
    --string "John Doe"           : Searches for amount of occurances of "John Doe" on each page
    --regex  "^\d{3}\s?\d{3}$"    : Searches for any values that matches the provided regular expression
    --fuzz                        : Turns on page fuzzing which searchs for over 4000 common pages
    --fuzz_subdomains             : Turns on subdomain fuzzing which searchs for various common subdomains
```
This does not represent all of the custom scan options available, but should give a snapshot of what Arachnid can do. For a full breakdown on each option please refer to the full documentation.

## Installation
Arachnid requires [pip](https://pypi.org/project/pip/) to install and [PHP](https://www.php.net/) to run properly.
* Install pip with the following commands
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

* Installing PHP varies by operating system. If you're on a Unix system your default package repository likely contains it and you'll simply need to install it there. No configuration is required. For further instructions, refer to the [offical documentation](https://www.php.net/manual/en/install.php).
* Then simply install Arachnid via pip.
```
pip install arachnid-crawler
```

## Disclaimer 
Arachnid is a OSINT tool build to aid penetration testers, web developers, and system admins to scan an authorized domain for data leakage. While there is nothing inherently illegal about scanning or scraping information from a website users should use caution when using this tool:

**Scanning and scraping can be considered the pretext to an attack**. Some security teams consider any OSINT recon the pretext to an attack and may pursue criminal charges if they are able to identify the source of the scans. 

**Aggressive scans might inadvertently cause a DoS**. This tool could possibly send out thousands of requests to a given server (depending on the size of the website and the fuzzing level set). If the server is not configured to handle that much bandwidth then this tool may inadvertently result in causing a denial-of-service (DoS). Even if it is unintentional, this could result in criminal charges. 

**This tool does not hide your identity**. While the stealth scans might modify the header information and timing to avoid IPS/IDS detection, it does not do anything to spoof or obfuscate the origin of the request. If users want to make their requests anonymous then they should consider routing their traffic through something like TOR or a VPN. 

In short, only use this tool to scan targets that you are authorized to scan, and that you know can handle the scan types that you configure. By using this Arachnid you agree to not use this tool if engage in malicious activity or scan unauthorized targets. In addition, the authors and contributors of this project are not responsible for any malicious usage or damage caused by this tool.    
