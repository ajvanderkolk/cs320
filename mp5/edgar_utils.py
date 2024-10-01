import re
import netaddr
from bisect import bisect
import pandas as pd

ips_df = pd.read_csv("ip2location.csv")

def lookup_region(ipaddr):
    ipaddr = re.sub('[a-z]', '0', ipaddr)
    ip_int = int(netaddr.IPAddress(ipaddr))
    idx = bisect(ips_df['low'], ip_int) - 1
    location = ips_df.at[idx, 'region']
    return location

class Filing:
    def __init__(self, html):
        self.dates = self.__dates(html)
        self.sic = self.__sic(html)
        self.addresses = self.__addresses(html)
        self.html = html

    def __dates(self, html):
        dates = re.findall(r"\d{4}-[0-1]{1}[0-9]{1}-\d{2}", html)
        clean = []
        for d in dates:
            split = d.split('-')
            if (int(split[0][0:2]) <= 20) and (int(split[0][0:2]) >= 19):
                if int(split[1]) <= 12:
                    if int(split[2]) > 0:
                        clean.append(d)
        return clean

    def __sic(self, html):
        sic = re.findall(r"SIC=([0-9]{3,4})", html)
        try:
            sic = int(sic[0])
        except IndexError:
            sic = None
        return sic

    def __addresses(self, html):
        addresses = []
        for addr_html in re.findall(r'<div class="mailer">([\s\S]+?)</div>', html):
            lines = []
            for line in re.findall(r'<span class="mailerAddress">([.\s\S]+?)</span>', addr_html):
                lines.append(line.strip())
            addresses.append("\n".join(lines))
            
            if addresses[-1] == '':
                addresses = addresses[:-1]
        return addresses

    
    def state(self):
        for addr in self.addresses:
            abbrev = re.findall(r' ([A-Z]{2}) [0-9]{5}', addr)
            if len(abbrev) > 0:
                return abbrev[0]
            else:
                continue
            
        return None

state_temp = {'CA': 92,
 'NJ': 23,
 'MS': 1,
 'MA': 30,
 'CO': 25,
 'NY': 83,
 None: 56,
 'TX': 67,
 'FL': 21,
 'AL': 1,
 'IN': 5,
 'CT': 14,
 'UT': 5,
 'MD': 13,
 'KS': 5,
 'VA': 15,
 'OH': 10,
 'SD': 1,
 'DE': 9,
 'IL': 25,
 'GA': 9,
 'NC': 9,
 'PA': 25,
 'TN': 4,
 'MN': 15,
 'NM': 1,
 'KY': 2,
 'OK': 7,
 'AR': 1,
 'NV': 6,
 'VT': 1,
 'MO': 4,
 'MI': 11,
 'NE': 2,
 'IA': 6,
 'AZ': 5,
 'WI': 9,
 'LA': 2,
 'ID': 1,
 'OR': 2,
 'WV': 2,
 'WA': 3,
 'DC': 1,
 'ME': 1}
sic_temp = {2834: 984,
 1389: 656,
 1311: 550,
 2836: 429,
 6022: 379,
 1000: 273,
 6211: 237,
 7371: 229,
 2860: 226,
 6021: 204,
 2510: 171,
 6282: 171,
 3825: 164,
 4841: 108,
 5621: 99,
 7200: 94,
 7374: 94,
 6331: 91,
 5311: 90,
 6798: 90,
 3842: 87,
 6221: 85,
 6029: 83,
 3272: 81,
 3829: 73,
 4931: 70,
 3510: 66,
 7830: 62,
 3826: 56,
 3695: 55,
 3620: 50,
 7373: 48,
 6799: 46,
 4412: 43,
 4512: 42,
 7340: 40,
 900: 39,
 7370: 39,
 3621: 38,
 6513: 38,
 5172: 36,
 4213: 35,
 5900: 35,
 3990: 34,
 5122: 34,
 2070: 33,
 5944: 33,
 8090: 32,
 1700: 31,
 4922: 31,
 3312: 31,
 1381: 31,
 6324: 30,
 8742: 27,
 7389: 26,
 8731: 25,
 7812: 25,
 3590: 24,
 3663: 23,
 4955: 23,
 4522: 22,
 6321: 21,
 3559: 20,
 6792: 19,
 5812: 19,
 6189: 18,
 7372: 16,
 3841: 14,
 6199: 11,
 1731: 11,
 4911: 8,
 6035: 7,
 4833: 7,
 2430: 6,
 3571: 6,
 3674: 5,
 3679: 5,
 4813: 4,
 4812: 4,
 3678: 4,
 5500: 4,
 1531: 4,
 6411: 3,
 3576: 3,
 8062: 3,
 2800: 3,
 3420: 3,
 1400: 3,
 2111: 2,
 7900: 2,
 5661: 2,
 6141: 2,
 5940: 2,
 1221: 2,
 8082: 2,
 3661: 2,
 1040: 2,
 6770: 2,
 3690: 2,
 5065: 2,
 3577: 2,
 2870: 2,
 8711: 2,
 3669: 2,
 1382: 2,
 2810: 2,
 2890: 2,
 3845: 2,
 6311: 2,
 6111: 1,
 2780: 1,
 2033: 1,
 2790: 1,
 5030: 1,
 3537: 1,
 3630: 1,
 2024: 1,
 7381: 1,
 100: 1,
 3443: 1,
 7363: 1,
 5160: 1,
 3730: 1,
 6200: 1,
 3585: 1,
 1623: 1,
 3550: 1,
 4924: 1,
 6036: 1,
 3711: 1,
 4899: 1,
 2273: 1,
 3827: 1,
 2820: 1,
 7384: 1,
 6099: 1,
 7320: 1,
 2842: 1,
 2750: 1,
 7311: 1,
 5990: 1,
 8093: 1,
 3578: 1,
 3714: 1,
 2030: 1,
 5531: 1,
 5731: 1,
 3721: 1,
 2670: 1,
 2911: 1,
 7990: 1,
 7350: 1,
 2711: 1,
 3541: 1,
 2080: 1,
 8200: 1,
 2320: 1,
 5651: 1,
 3672: 1,
 5945: 1,
 6500: 1,
 7361: 1,
 4941: 1,
 7330: 1,
 3442: 1,
 3490: 1,
 5961: 1,
 7841: 1,
 3140: 1,
 7822: 1,
 5960: 1,
 3944: 1,
 8051: 1,
 3317: 1}