# Arachnid 
Arachnid is an OSINT web crawler that targets a website, attempts to enumerate all of the pages within it, and then search for interesting or sensitive information both defined by the tool and/or the user. Arachnid is built in Python, and the data is visualized via a php web app. 

![Scan Dashboard](https://github.com/jake-bickle/Arachnid/blob/master/scan_dashboard_feature.png)

## Overview
Arachnid started with a simple question: “is there a way that users could find all the emails of a supplied domain to help with OSINT efforts?” This of course could only be answered by using a web crawler to visit and search every page in a given domain. But then followup questions arose: “if we are already visiting each page and looking for emails, couldn’t we look for other interesting information as well?” And thus, the idea for a fully developed OSINT web crawler was born.  Presently, the default scan for Arachnid searches for the following information:

* Email addresses
* Phone numbers
* Common documents and files
* Social Media Handles
* User supplied strings and regex (optional)

To help support scanning efforts, Arachnid also comes with some other features such as:

* The ability to choose a given user agent to make the scan requests
* The ability to add a delay to the scan requests as a mean to reduce scan noise
* The ability to fuzz for interesting files and directories as a mean to discover hidden information (similar to dirb)

## Installation
[Coming Soon]

## Basic usage
Arachnid can be hyper-customized to only search for information that is relevant to the user—however, it also comes preloaded with default scans that find generally useful or interesting information.  To use the default scan, users can simple issue the following command:

```
arachnid https://www.example.com/
```

This will launch a local php server that displays the visualized data. The output will be reloaded every 30 seconds to reflect newly found information. 

## Predefined Scan Types
To help make this tool more useful, in addition to the default scan listed above, there are a few other preconfigured scan types that users can make use of.

### “Stealth” Scan
```
arachnid https://example.com --stealth
```
A stealth scan will use the Google bot user agent, masking the crawler  instead of a regular firefox user. It also has a substantial delay between page requests to help make the scan less noisy. **This scan has the potential to take a long time to finish**

### “Aggressive” Scan
```
arachnid https://example.com --aggressive
```

An aggressive scan will ignore robots.txt rules and crawl all pages found on it. Aggressive also enables fuzzing for many pages and subdomains, and crawls at the fastest possible speed. This is ideally used when triggering alerts_IDS_WAF is not a concern. 

### “Page Only” Scan
```
arachnid https://example.com/example_page.php --page-only
```

Users can scrape a ingle web page instead of imitating a full site crawl. This is ideal if users want to scrape sensitive information from a data-rich page (such as a web directory)

All predefined scan types are only a base plate of options. Users may override any options they provide by supplying additional arguments. 

## Custom Scans
Arachnid also allows users very granular control over how they want to scan to run. Here is a sample custom scan:
```
arachnid https://example.com --aggressive --find docs phone --agent y --delay medium --doc ".psd" --string "John Doe" --regex "^\d{3}\s?\d{3}$" --fuzz --fuzz_subdomains

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

This does not represent all of the custom scan options available, but should give a snapshot of what Arachnid can do. For a full breakdown on each option please refer to the full documentation or use **arachnid —help**.

## Disclaimer
Arachnid is a OSINT tool built to aid penetration testers, web developers, and system admins to scan an authorized domain for data leakage. While there is nothing inherently illegal about scanning or scraping information from a website users should use caution when using this tool:
**Scanning and scraping can be considered the pretext to an attack**. Some security teams consider any OSINT recon the pretext to an attack and may pursue criminal charges if they are able to identify the source of the scans.

**Aggressive scans might inadvertently cause a DoS**. This tool could possibly send out thousands of requests to a given server (depending on the size of the website and the fuzzing level set). If the server is not configured to handle that much bandwidth then this tool may inadvertently result in causing a denial-of-service (DoS). Even if it is unintentional, this could result in criminal charges.

**This tool does not hide your identity**. While the stealth scans might modify the header information and timing to avoid IPS/IDS detection, it does not do anything to spoof or obfuscate the origin of the request. If users want to make their requests anonymous then they should consider routing their traffic through something like TOR or a VPN.
In short, only use this tool to scan targets that you are authorized to scan, and that you know can handle the scan types that you configure. By using this Arachnid you agree to not use this tool if engage in malicious activity or scan unauthorized targets. In addition, the authors and contributors of this project are not responsible for any malicious usage or damage caused by this tool.
