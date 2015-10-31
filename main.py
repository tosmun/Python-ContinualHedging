#!/usr/bin/python

# Commandline args
import sys, argparse

from ch import logger, config

NAME="ContinualHedging"

arg_parser = argparse.ArgumentParser(description=NAME)
arg_parser.add_argument('--config', action='store',
                        dest='configFile',
                        default='./ContinualHedging.properties',
                        required=False, help='Path to py properties file.'+
                        'File encoding is assumed to be UTF-8')

def usage(msg):
    print('Error: %s' % msg)
    arg_parser.print_usage()
    exit(2)

def main():
    args = arg_parser.parse_known_args(sys.argv[1:])[0]
    # Read configuration
    configuration = config.Configuration(path=args.configFile)
    # Grab a logger
    log = logger.Log(configuration, NAME)
    if log.isDebugEnabled():
        log.debug("%s initialized" % NAME)
    from ch.apis import stockprice
    spr = stockprice.StockPriceRequests(configuration)
    print(spr.getStockPriceData().getLastTradePrice())
    exit(0)

if __name__ == "__main__":
    main()