import dns.resolver
from dns import reversename, resolver
from read_config import read_dns_server

def look_up(name, ntype=["A", "AAAA", "MX", "NS", "SOA"]) -> str|list:

    if not "." in name:
        name = f"{name}.local"

    try:
        answer = dns.resolver.Resolver()
        answer.nameservers = read_dns_server().split(",")
        ans_list = []

        for qtype in ntype:
            try:
                ans = answer.resolve(name, qtype, raise_on_no_answer=False, lifetime=15)
                ans_list.append(ans.rrset)
            except dns.resolver.LifetimeTimeout as err:
                return err
        if None in ans_list:
            ans_list.pop(ans_list.index(None))
        return ans_list

    except ValueError as err:
        return err

    except dns.resolver.NXDOMAIN:
        try:
            rev = dns.reversename.from_address(name)
            rev_adres = resolver.resolve(rev, "PTR")
            return rev_adres.rrset
        except dns.exception.SyntaxError:
            return f"The DNS query name does not exist: {name}"
