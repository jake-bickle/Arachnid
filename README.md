# Arachnid
An OSINT web crawling tool to find data leakage on a target websites using advanced web scraping and parsing technology.

---
![A picture of the user interface in its early stages](/output_early_showcase.png?raw=true)
## What is Arachnid?
Arachnid is a powerful web crawler that has been refined to effectively accomplish two things: aggressively find and index all of the pages of a target domains (and its subdomains) while also searching for "interesting" data on each page as it crawls. A default scan will search for the following:
* Email addresses
* Phone numbers
* Common documents and files
* Social Media Handles

In addition, users can supply their own custom regular expressions, strings, or custom file extensions to scrape as well. Preconfigured scans allow users to quickly begin using the tool, while custom scan allow users to build a highly individual scan that fits their target.

## Arachnid Usage

### Defualt Scan
The default usage for Arachnid is as follows:
> python3 -m arachnid https://example.com

This will scan using the default configuration which includes:
* Scrape for the following things:
  * Emails
  * Phone numbers
  * Social media Handles
  * Common documents and file types
* Crawls and indexes all pages on the domain
* It will ignore the robots.txt files
* Uses the default Firefox user agent header
* Uses no delay when crawling
* Fuzzes for interesting pages on LOW

### Other Predefined Scan Types
To help make this tool more useful, there are also two other preconfigured scan types that you can make use of: stealth and aggressive scans.

**Stealth scan**
> python3 -m arachnid https://example.com --stealth

See documentation for the full config of this scan--however, the general difference is that it uses no fuzzing, adds a delay, and uses a SearchBot agent header. This is supposed to help avoid detection from an IDS/IPS.  

**Aggressive Scan**
> python3 -m arachnid https://example.com --aggressive

The aggressive scan adds a much higher degree of fuzzing (over 30,000 tries), includes no delay.

### Custom Scans
Arachnid also allows users very granular control over how they want to scan to run. Here is a sample custom scan:
> python3 -m arachnid.py https://example.com --find docs phone --agent y --delay medium --doc ".psd" --string "John Doe" --regex "^\d{3}\s?\d{3}$" --fuzz high

Here is that scan broken down into its parts:
```
    https://example.com           : Required argument, specifies the domain to target
    --find docs phone             : Only scrapes for common documents and phone numbers
    --agent y                     : Uses the Yahoo SearchBot header sting
    --delay medium                : Sets the timing delay to medium, which is between 4 to 11 seconds
    --doc ".psd"                  : In addition to common docs, the crawler will also look for .psd file
    --string "John Doe"           : Searches for amount of occurances of "John Doe" on each page
    --regex  "^\d{3}\s?\d{3}$"    : Searches for any values that matches the provided regular expression
    --fuzz high                   : Sets the fuzzing level to fuzz for 'interesting' 10,000 pages
```
This does not represent all of the custom scan options available, but should give a snapshot of what Arachnid can do. For a full breakdown on each option please refer to the full documentation.

## Disclaimer 
Arachnid is a OSINT tool build to aid penetration testers, web developers, and system admins to scan an authorized domain for data leakage. While there is nothing inherently illegal about scanning or scraping information from a website users should use caution when using this tool:

**Scanning and scraping can be considered the pretext to an attack**. Some security teams consider any OSINT recon the pretext to an attack and may pursue criminal charges if they are able to identify the source of the scans. 

**Aggressive scans might inadvertently cause a DoS**. This tool could possibly send out thousands of requests to a given server (depending on the size of the website and the fuzzing level set). If the server is not configured to handle that much bandwidth then this tool may inadvertently result in causing a denial-of-service (DoS). Even if it is unintentional, this could result in criminal charges. 

**This tool does not hide your identity**. While the stealth scans might modify the header information and timing to avoid IPS/IDS detection, it does not do anything to spoof or obfuscate the origin of the request. If users want to make their requests anonymous then they should consider routing their traffic through something like TOR or a VPN. 

In short, only use this tool to scan targets that you are authorized to scan, and that you know can handle the scan types that you configure. By using this Arachnid you agree to not use this tool if engage in malicious activity or scan unauthorized targets. In addition, the authors and contributors of this project are not responsible for any malicious usage or damage caused by this tool.    
