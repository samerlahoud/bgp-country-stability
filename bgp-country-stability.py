#!/root/anaconda3/bin/python
import json
import requests
import sys

api_url_base = 'https://stat.ripe.net/data/'

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

    api_url = '{}bgp-update-activity/data.json?resource={}&starttime=2018-02-06T12:00'.format(api_url_base, asn)

    response = requests.get(api_url)

    if response.status_code == 200:
        bgp_activity = json.loads(response.content.decode('utf-8'))
        nb_announcements = sum(s['announcements'] for s in bgp_activity["data"]["updates"] if s['announcements']!=
 None)
        nb_withdrawals = sum(s['withdrawals'] for s in bgp_activity["data"]["updates"] if s['withdrawals']!= None)
        nb_updates = nb_announcements+nb_withdrawals
        return [nb_updates, nb_announcements, nb_withdrawals]
    else:
        return None

def get_country_update(country_code):

    #country_asn_list = [9051, 39010, 42020]
    country_asn_list = get_country_asn(country_code)
    country_update = {}
    for asn in country_asn_list:
        country_update[asn] = get_asn_update(asn)[0]
    return country_update

if __name__ == "__main__":
    
    print(get_country_update(str(sys.argv[1])))
    #for asn in country_asn_list:
    #    print('AS{} is guilty of {}'.format(asn,get_asn_update(asn)[0]))
