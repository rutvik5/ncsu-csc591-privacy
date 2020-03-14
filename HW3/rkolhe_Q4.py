"""Reads a har file from the filesystem, converts to CSV, then dumps to
stdout.
"""
import argparse
import json
from urllib.parse import urlparse
from tld import get_tld
import networkx as nx
import matplotlib.pyplot as plt
from adblockparser import AdblockRules

def readfile(filename):
    rules = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            rules.append(line)
    return rules

def main(harfile_path):
    """Reads a har file from the filesystem, converts to CSV, then dumps to
    stdout.
    """
    txt_file = 'easylist.txt'
    raw_rules = readfile(txt_file)

    harfile = open(harfile_path, encoding  = 'UTF-8')
    harfile_json = json.loads(harfile.read())
    i = 0

    first_party = harfile_path.split('.')[1]+'.'+harfile_path.split('.')[2]
    rules = AdblockRules(raw_rules)
    blocked = 0
    blocked_domains = set()
    opt = {'script': True,'image':True,'stylesheet':True,'object':True,'subdocument':True,'xmlhttprequest':True,'websocket':True,'webrtc':True,'popup':True,'generichide':True,'genericblock':True}
    
    for entry in harfile_json['log']['entries']:
        i = i + 1
        url = entry['request']['url']
        urlparts = urlparse(entry['request']['url'])
        size_bytes = entry['response']['bodySize']
        size_kilobytes = float(entry['response']['bodySize'])/1024
        mimetype = 'unknown'
        if 'mimeType' in entry['response']['content']:
            mimetype = entry['response']['content']['mimeType']
        
        option = ''
        res = get_tld(url, as_object=True)
        mime_opt = mimetype.split('/')[0]

        if mime_opt in opt:
        	option = mime_opt
        
        if res.fld != first_party and option in opt and rules.should_block(url, {option: opt[option]}):
        	blocked += 1
        	blocked_domains.add(res.fld)
    
    blocked_domains = [dom for dom in blocked_domains] if blocked_domains else 'No domains blocked'

    print(f'\nSite: {first_party}\n# of total HTTP requests: {i}\n# of HTTP requests blocked: {blocked}\nBlocked domains: {blocked_domains}\n')

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        prog='parsehar',
        description='Parse .har files into comma separated values (csv).')
    argparser.add_argument('harfile', type=str, nargs=3,
                        help='path to harfile to be processed.')
    args = argparser.parse_args()
    
    # main(args.harfile[0])
    for idx in range(3):
    	harfile_path = args.harfile[idx]
    	first_party = harfile_path.split('.')[1]+'.'+harfile_path.split('.')[2]
    	print(f'\nProcessing {first_party}...')
    	main(harfile_path)
    	print(f'Completed {first_party}!')