# WebFaction Dynamic DNS

Update a WebFaction domain with the public IP address of your Internet connection.

[source @ github](https://github.com/wamonite/webfaction_dyndns)

## Configuration

Prior to running, create the domain via the WebFaction control panel, set it to 'External' and set an initial IP address.

When running, the following environment variables need to be set:-

* `WEBFACTION_DYNDNS_DOMAIN`

	domain excluding `http://` or `https://`
	
* `WEBFACTION_DYNDNS_USER_NAME`

	WebFaction control panel user name
	
* `WEBFACTION_DYNDNS_PASSWORD`

	WebFaction control panel password

Protect your password using a tool such as `envdir`, e.g.

	envdir ~/envdir/dyndns_config ./webfaction_dyndns.py -q
	
## Usage

	usage: webfaction_dyndns.py [-h] [-q]

	optional arguments:
      -h, --help   show this help message and exit
      -q, --quiet  only output on error
  
## Prerequisites

* Python 2.7
* Python 2.6 with `argparse` module

## License

Copyright (c) 2014 Warren Moore

This software may be redistributed under the terms of the MIT License.
See the file LICENSE for details.

## Contact

          @wamonite     - twitter
           \_______.com - web
    warren____________/ - email
