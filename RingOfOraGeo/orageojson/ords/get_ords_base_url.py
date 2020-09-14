import re, os

# get the ORDS Common Base URL

def find_match(tns_regex, y):
    x1 = re.match(tns_regex, y, re.M + re.I + re.S)
    if x1 is not None:
        x1 = x1.groups(1)[0] # Only first match is returned
        x1 = x1.strip('\n')
    return(x1)

def get_ords_base_url():

    if os.environ.get('TNS_ADMIN') is None:
        raise Exception('$$$ Error: Cannot find TNS_ADMIN as system variable')
    else:
        try:
            tns_file = open(os.environ.get('TNS_ADMIN') + "/tnsnames.ora", "r")
        except IOError as err:
            raise IOError('$$$ Error: Cannot find tnsnames.ora in TNS_ADMIN location')

    lines = tns_file.readlines()
    for line in lines:
        if not line.startswith('#'):
            tnsnames_ = re.split(r"\){3,}\n\n", line)
            break

    # Regex matches
    tns_host_ = '.*?HOST\s?=\s?(.+?)\)'
    tns_sname_ = '.*?SERVICE_NAME\s?=\s?(.+?)\)'

    tns_dir_ = []

    for y in tnsnames_:
        y = '%s))' % y
        l = [find_match(x, y) for x in [tns_host_, tns_sname_]]
        d = {
            'host': l[0],
            'service': l[1],
        }
        tns_dir_.append(d)

    # print(tns_dir_[0].get('host'))
    # print(tns_dir_[0].get('service'))

    url = str

    url_ = 'https://' + tns_dir_[0].get('service').split('_')[0] + \
           '-' + tns_dir_[0].get('service').split('_')[1] + \
           '.' + tns_dir_[0].get('host').replace('.com', 'apps.com') + '/ords/'

    return url_

# test it.
if __name__ == '__main__':
    get_ords_base_url()



