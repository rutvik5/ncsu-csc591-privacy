import argparse
import json
from urllib.parse import urlparse
from tld import get_tld
import networkx as nx
import matplotlib.pyplot as plt

def main(harfile_path):
    """Reads a har file from the filesystem, converts to CSV, then dumps to
    stdout.
    """
    harfile = open(harfile_path, encoding  = 'UTF-8')
    harfile_json = json.loads(harfile.read())
    i = 0
    domain_set = set()

    for entry in harfile_json['log']['entries']:
        i = i + 1
        url = entry['request']['url']
        urlparts = urlparse(entry['request']['url'])
        size_bytes = entry['response']['bodySize']
        size_kilobytes = float(entry['response']['bodySize'])/1024
        mimetype = 'unknown'
        if 'mimeType' in entry['response']['content']:
            mimetype = entry['response']['content']['mimeType']

        # print ('%s,"%s",%s,%s,%s,%s' % (i, url, urlparts.hostname, size_bytes,
        #                                size_kilobytes, mimetype))

        res = get_tld(url, as_object=True)
        domain_set.add(res.fld)
        
    
    first_party = harfile_path.split('.')[1]+'.'+harfile_path.split('.')[2]
    if first_party in domain_set:
    	domain_set.remove(first_party)
    
    print(f'\n{first_party}- Third Party Domains:\n{domain_set}')

    g = nx.Graph()
    for val in domain_set:
    	g.add_edge(first_party, val)

    nx.draw(g, with_labels = True)
    plt.show()

    

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        prog='parsehar',
        description='Parse .har files into comma separated values (csv).')
    argparser.add_argument('harfile', type=str, nargs=3,
                        help='path to harfile to be processed.')
    args = argparser.parse_args()

    for idx in range(3):
    	main(args.harfile[idx])