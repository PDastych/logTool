#! /usr/bin/python3

import argparse
from modules import db
import re
import config



def main():
    parser = argparse.ArgumentParser(description='Log analyzer')
    parser.add_argument('table', type=str,help='Provide your database name')
    parser.add_argument('-u', '--update', type=str, help='Update your database with new logs')
    parser.add_argument('-d', '--delete', action='store_true', help='Delete whole database')
    parser.add_argument('-s', '--show_all', action='store_true', help='Show all ips stored in database')
    parser.add_argument('-l', '--list', action='store_true', help='List all dangerous ips')
    parser.add_argument('-r', '--ranking', type=int, help='Make a ranking of most dangerous ips')
    parser.add_argument('-i', '--ip_info', type=str, nargs='+', help='Show information about specified ips')
    parser.add_argument('--remove_ip', type=str, nargs='*', help='Remove specified ips')
    parser.add_argument('--remove_dangerous', action='store_true', help='Remove dangerous ips from database')
    args = parser.parse_args()
    if args.table:
        try:
            db.create_table(args.table)
            print('New database created')
        except:
            pass

    if args.delete:
        db.delete_table(args.table)
        print('Database deleted')

    if args.update:
        db.update_data(args.table, get_failed_attempts(args.update), get_correct_attempts(args.update), config.ban_number)
        print('Database updated')

    if args.show_all:
        db.get_all_ip(args.table)

    if args.list:
        for i in db.get_dangerous_ip(args.table):
            print(i)
    if args.ranking:
        db.print_ip_ranking(args.table, args.ranking)

    if args.ip_info:
        db.print_information_by_ip(args.table, args.ip_info)

    if args.remove_ip:
        db.delete_row_by_ip(args.table, args.remove_ip)
        print('Ips Removed')

    if args.remove_dangerous:
        db.delete_row_by_ip(args.table, db.get_dangerous_ip(args.table))

def get_failed_attempts(path):
    with open(path) as file:
        x = file.read()
    ip_results = re.findall('Invalid user \S+ from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', x)
    ip_results.extend(re.findall('Failed password for \S+ from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', x))
    return ip_results



def get_correct_attempts(path):
    with open(path) as file:
        x = file.read()
    ip_accepted = re.findall('Accepted \S+ for \S+ from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', x)
    return ip_accepted



if __name__ == '__main__':
    main()
