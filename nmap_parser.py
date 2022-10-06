import requests
import argparse 

def get_between(string, x, y):
    return string.split(x)[1].split(y)[0].strip()

def load_file(path):
    return open(path,'r').readlines()

def get_web_content(url):
    return requests.get(url).text

def create_dict(line):
    url = get_between(line, "Nmap scan report for ", " (")
    ip = get_between(line, '(', ')')
    return {"url":url,"ip":ip}

def parse_dict(my_dict, i1, i2):
    return my_dict[i1] + ": " + my_dict[i2] 

def main(args):
    undocumented = []
    nmap_scan_data = load_file(args['input_file'])
    crud_db_page = get_web_content(args['url'])
    for line in nmap_scan_data:
        if "Nmap scan report for " in line:
            temp_dict = create_dict(line)
            if not temp_dict["ip"] in crud_db_page:
                undocumented.append(parse_dict(temp_dict,"url","ip"))
    if args["output_file"]:
        with open(args["output_file"], 'w') as f:
            for undoc_item in undocumented:
                f.write(f'{undoc_item}\n')
    else:
        for undoc_item in undocumented:
            print(undoc_item)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This script is used to find discrepancies between what\'s documented in a CRUD database and what shows up in an NMAP scan')
    parser.add_argument('-u','--url', help='Specifies the URL of CRUD database to check against', required=True)
    parser.add_argument('-i','--input-file', help='Specifies the file of NMAP output to parse through', required=True)
    parser.add_argument('-o', '--output_file', help='Specifies the path and filename you\'d like to save the results as', required=False)
    args = vars(parser.parse_args())
    main(args)
