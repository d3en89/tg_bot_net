import dns.resolver
from dns import reversename, resolver

def look_up(name, ntype=['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'MX']):
    try:
        for qtype in ntype:
            answer = dns.resolver.resolve(name,qtype, raise_on_no_answer=False)
            answer.nameservers=['name_server']
            if answer.rrset is not None:
                return answer.rrset
    except dns.resolver.NXDOMAIN:
        rev = dns.reversename.from_address(name)
        rev_adres = str(resolver.resolve(rev,"PTR")[0])
        return rev_adres

