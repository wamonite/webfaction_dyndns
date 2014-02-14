#!/usr/bin/env python
'''
WebFaction Dynamic DNS

Update a WebFaction domain with the public IP address of your
Internet connection.

2014/02/07

Warren Moore
      @wamonite     - twitter
       \_______.com - web
warren____________/ - email
'''

##################################################################
# Imports
 
import os
import xmlrpclib
import urllib2
import json
import argparse

##################################################################
# Functions
 
class ScriptException(Exception):
    pass
    
def get_arguments():
    '''Process command-line arguments
    '''
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-q",
                        "--quiet",
                        help = "only output on error",
                        action = "store_true")
    args = parser.parse_args()

    return args.quiet
        
def get_settings():
    '''Get settings from environment variables
    '''
    
    try:
        domain_name = os.environ['WEBFACTION_DYNDNS_DOMAIN']
        user_name = os.environ['WEBFACTION_DYNDNS_USER_NAME']
        password = os.environ['WEBFACTION_DYNDNS_PASSWORD']
        
    except KeyError:
        raise ScriptException('Please ensure WEBFACTION_DYNDNS_DOMAIN, '
                              'WEBFACTION_DYNDNS_USER_NAME and '
                              'WEBFACTION_DYNDNS_PASSWORD environment '
                              'variables are defined')
    
    return domain_name, user_name, password
    
def webfaction_login(user_name, password):
    '''Get the XMLRPC server and session for the WebFaction API
    '''
    
    server = xmlrpclib.ServerProxy('https://api.webfaction.com/')
    session_id, account = server.login(user_name, password)
    
    return server, session_id

def get_domain_address(server, session_id, domain_name):
    '''Get the overridden IP address for the provided domain name
    '''
    
    try:
        domain_override_list = server.list_dns_overrides(session_id)
        for domain_override in domain_override_list:
            if domain_name == domain_override['domain']:
                domain_address = domain_override['a_ip']
                
        return domain_address

    except (UnboundLocalError, KeyError):
        raise ScriptException("Please configure the external IP address for '%s' "
                              "via the WebFaction control panel" % (domain_name))
    
def update_domain_address(server,
                          session_id,
                          domain_name,
                          domain_address,
                          public_address):
    '''Remove the old and set the new IP address for the domain name
    '''
    
    server.delete_dns_override(session_id, domain_name, domain_address)
    server.create_dns_override(session_id, domain_name, public_address)

def get_public_address():
    '''Get the public IP address (from http://jsonip.com)
    '''
    
    page = urllib2.urlopen('http://jsonip.com/')
    page_json = json.loads(page.read())
        
    return page_json['ip']

def get_log_function(quiet):
    '''Bake in log function behaviour
    '''
    
    def log_function(message):
        if not quiet:
            print message
    
    return log_function
    
def check_domain_address():
    '''Check the domain address and update if required
    '''
    
    quiet = get_arguments()
    
    log = get_log_function(quiet)
    
    dynamic_domain_name, user_name, password = get_settings()
    
    public_address = get_public_address()
    log('Public address: %s' % public_address)
    
    server, session_id = webfaction_login(user_name, password)
    log("Login successful for '%s'" % user_name)

    domain_address = get_domain_address(server,
                                        session_id,
                                        dynamic_domain_name)
    log("Current address for '%s': %s" % (dynamic_domain_name,
                                          domain_address))
    
    if public_address != domain_address:
        update_domain_address(server,
                              session_id,
                              dynamic_domain_name,
                              domain_address,
                              public_address)
        log('Domain updated: %s -> %s' % (domain_address, public_address))

##################################################################
# Main
 
if __name__ == "__main__":
    try:
        check_domain_address()

    except ScriptException as e:
        print 'Error:', e
