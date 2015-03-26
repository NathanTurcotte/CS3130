#!/usr/bin/env python3

import argparse, Client, Server

def s(ip, port):
    Server.server(ip, port)
def c(ip, port):
    Client.client(ip,port)

if __name__ == '__main__':
    choices = {'client':c, 'server':s}
    parser = argparse.ArgumentParser(description='Messaging System')
    parser.add_argument('role', choices=choices, help='Server or Client?')
    parser.add_argument('host', help='Server IP')
    parser.add_argument('-p', metavar='PORT', type=int, default=2015,
                        help='UDP port(default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)


