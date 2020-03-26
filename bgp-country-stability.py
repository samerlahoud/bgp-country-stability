#!/root/anaconda3/bin/python
import json
import requests
import sys
from time import gmtime, strftime
from datetime import date, timedelta

api_url_base = 'https://stat.ripe.net/data/'

starttime = date.today()+timedelta(weeks=-4)
endtime = date.today()+timedelta(weeks=-2)

starttime = starttime.strftime("%Y-%m-%dT12:00")
endtime = endtime.strftime("%Y-%m-%dT12:00")

def get_country_asn(country_code):

    api_url = '{}country-asns/data.json?resource={}&lod=1'.format(api_url_base, country_code)

    response = requests.get(api_url)

    if response.status_code == 200:
        country_asns_json = json.loads(response.content.decode('utf-8'))
        country_asns = country_asns_json["data"]["countries"][0]["routed"]
        return country_asns
    else:
        return None

def get_asn_update(asn):

    api_url = '{}bgp-update-activity/data.json?resource={}&starttime={}&endtime={}'.format(api_url_base, asn, starttime, endtime)

    response = requests.get(api_url)

    if response.status_code == 200:
        bgp_activity = json.loads(response.content.decode('utf-8'))
        nb_announcements = sum(s['announcements'] for s in bgp_activity["data"]["updates"] if s['announcements']!= None)
        nb_withdrawals = sum(s['withdrawals'] for s in bgp_activity["data"]["updates"] if s['withdrawals']!= None)
        nb_updates = nb_announcements+nb_withdrawals
        return [nb_updates, nb_announcements, nb_withdrawals]
    else:
        return None

def get_asn_prefix(asn):

    api_url = '{}announced-prefixes/data.json?resource={}&starttime={}&endtime={}'.format(api_url_base, asn, starttime, endtime)

    response = requests.get(api_url)

    if response.status_code == 200:
        asn_prefix_list = json.loads(response.content.decode('utf-8'))
        nb_prefixes = len(asn_prefix_list["data"]["prefixes"])
        return nb_prefixes
    else:
        return None

def get_country_update(country_code):

    country_asn_list = get_country_asn(country_code)
    country_update = {}
    for asn in country_asn_list:
        country_update[asn] = get_asn_update(asn)[0]
    return country_update

if __name__ == "__main__":

    country_update = get_country_update(str(sys.argv[1]))
    outfile_path = './output/bgp-stability-{}-{}.txt'.format(str(sys.argv[1]),strftime("%Y-%m-%d", gmtime()))
    outfile = open(outfile_path, mode='w', encoding='utf-8')
    for asn in country_update:
        asn_prefix = get_asn_prefix(asn)
        asn_update = country_update[asn]
        outfile.write('{},{},{}\n'.format(asn,asn_update,asn_prefix))
    outfile.close()
