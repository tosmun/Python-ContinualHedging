#!/usr/bin/python
import sys, argparse
from ch import Daemon

arg_parser = argparse.ArgumentParser(description='ContinualHedging')
arg_parser.add_argument('--config', action='store',
                        dest='configFile',
                        default='./ContinualHedging.properties',
                        required=False, help='Path to py properties file.'+
                        'File encoding is assumed to be UTF-8')

def main():
    args = arg_parser.parse_known_args(sys.argv[1:])[0]
    d = Daemon(configFilePath=args.configFile)
    d.run()
    exit(0)

if __name__ == "__main__":
    main()