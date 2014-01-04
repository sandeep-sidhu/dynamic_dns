#!/usr/bin/python

from Foundation import CFRunLoopAddSource, CFRunLoopGetCurrent
from Foundation import kCFRunLoopCommonModes
from Foundation import CFRunLoopRun, CFRunLoopAddTimer
from Foundation import CFRunLoopTimerCreate, CFAbsoluteTimeGetCurrent
from SystemConfiguration import SCDynamicStoreCreate
from SystemConfiguration import SCDynamicStoreCopyValue
from SystemConfiguration import SCDynamicStoreSetNotificationKeys
from SystemConfiguration import SCDynamicStoreCreateRunLoopSource

import pyrax
import optparse
import logging
import ConfigParser

log = logging.getLogger(__name__)
	

class Watcher(object):
    def __init__(self, rax_username, rax_apikey, domain_name,
                 dns_record):
        pyrax.set_setting("identity_type", "rackspace")
        pyrax.set_credentials(rax_username, rax_apikey)
        self.dns = pyrax.cloud_dns

        store = self.store = SCDynamicStoreCreate(None,
            "global-network-watcher", self.dynamicStoreChanged, None)

        SCDynamicStoreSetNotificationKeys(
            store, None, ['State:/Network/Interface/en0/IPv4'])
        source = self.source = SCDynamicStoreCreateRunLoopSource(
            None, store, 0)

        loop = self.loop = CFRunLoopGetCurrent()
        CFRunLoopAddSource(loop, source, kCFRunLoopCommonModes)
        CFRunLoopRun()

    def _find_record(self, dom, record_name):
        for rec in self.dns.get_record_iterator(dom):
            if rec.name == record_name:
                log.debug("DNS record '%s' found." % rec.name)
                return rec

    def _find_domain(self, domain_name):
        for dom in self.dns.get_domain_iterator():
            if dom.name == domain_name:
                log.debug("Domain '%s' found." % domain_name)
                return dom

    def update_record(self, domain_name, record_name, ip_addr):
        dom = self._find_domain(domain_name)
        if not dom:
            log.error("Couldn't find domain.")
        rec = self._find_record(dom, record_name)
        if rec:
            dom.update_record(rec, data=ip_addr)
            log.info("DNS record updated. %s => %s" % (rec.name, rec.data))
        else:
            log.error("Couldn't find the record.")

    def get_ip_addr(self, store=None):
        store = store or self.store
        val = SCDynamicStoreCopyValue(
            store, 'State:/Network/Interface/en0/IPv4')
        if val:
            log.debug("value:%s" % val)
            data = dict(val)
            log.debug("Addresses:%s" % data['Addresses'])
            return list(data['Addresses'])
        else:
            return []

    def dynamicStoreChanged(self, store, changedKeys, info):
        for key in list(changedKeys):
            ip_addr = self.get_ip_addr(store)
            if ip_addr:
                log.debug("Interface en0 address:%s" % ip_addr)
                log.info("Updating dns record...")
                self.update_record(
                    "spsidhu.com", "ssidhu-mb.spsidhu.com", ip_addr[0])
            else:
                log.info("No IP address on en0")

def dummy_timer(*args):
    pass


def setup_logging(log_file=None, log_level=None):
    if log_file is None:
        log_file = "./dynamic_dns.log"
    if log_level is None:
        log_level = "DEBUG"

    log_format = '%(asctime)18s - %(levelname)8s - %(message)s'
    log_datefmt = '%m/%d/%Y %I:%M:%S %p'
    logging.basicConfig(format=log_format, datefmt=log_datefmt,
                        filename=log_file,
                        level=logging.getLevelName(log_level))
    
    formatter = logging.Formatter(log_format, datefmt=log_datefmt)
    
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)
    
    log.setLevel(logging.getLevelName(log_level))
    log.debug("DEBUG level enabled")


def main(options):
    config = ConfigParser.ConfigParser()
    config.readfp(open(options.config_file))
    log_level = config.get('main', 'log_level')
    log_file = config.get('main', 'log_file')
    rax_username = config.get('cloud_dns', 'username')
    rax_apikey = config.get('cloud_dns', 'apikey')
    domain_name = config.get('cloud_dns', 'domain_name')
    dns_record = config.get('cloud_dns', 'dns_record')
    
    # Setup logging
    setup_logging(log_file, log_level)

    # this gives us a callback into python every 1s for signal handling
    CFRunLoopAddTimer(CFRunLoopGetCurrent(),
        CFRunLoopTimerCreate(None, CFAbsoluteTimeGetCurrent(), 1.0, 0, 0,
            dummy_timer, None),
        kCFRunLoopCommonModes)
    try:
        log.info("IP Watcher started.")
        Watcher(rax_username, rax_apikey, domain_name, dns_record)
    except KeyboardInterrupt, e:
        log.info("Keyboard Interrupt, exiting: %s" % e)
        pass

if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage)
    parser.add_option('-c', '--config_file', dest='config_file',
        help='config_file to use')
    opts, args = parser.parse_args()
    if not opts.config_file:
        parser.error("config conf must be specified")

    main(opts)