import dns.resolver
from dns import reversename, resolver
from read_config import read_dns_server, read_dns_suffix


def look_up(name, ntype=['A', 'AAAA', 'MX', 'NS', 'SOA']) -> list | str:
    if not "." in name and read_dns_suffix()[0] == "True":
        name = f'{name}{read_dns_suffix()[1]}'

    try:
        answer = dns.resolver.Resolver()
        answer.nameservers = read_dns_server().split(",")
        ans_list = []

        for qtype in ntype:
            try:
                ans = answer.resolve(name, qtype, raise_on_no_answer=False, lifetime=15)
                ans_list.append(ans.rrset)
            except dns.resolver.LifetimeTimeout as err:
                return str(err)

        if None in ans_list:
            ans_list.pop(ans_list.index(None))
        return ans_list

    except ValueError as err:
        return str(err)

    except dns.resolver.NXDOMAIN:
        try:
            rev = dns.reversename.from_address(name)
            rev_adres = resolver.resolve(rev, "PTR")
            return rev_adres.rrset
        except dns.exception.SyntaxError:
            return f"The DNS query name does not exist: {name}"
        except dns.resolver.NXDOMAIN as err:
            return str(err)

