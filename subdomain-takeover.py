import requests
import dns.resolver

# Define the target domain
target_domain = "example.com"

# Define the list of service providers to check
service_providers = ["aws", "azure", "cloudflare", "github", "heroku"]

# Loop through the list of subdomains to check
for service in service_providers:
    subdomain = "{}.{}".format(service, target_domain)
    
    # Check if the subdomain is in use
    try:
        answers = dns.resolver.query(subdomain, 'CNAME')
        cname = answers[0].target.to_text()
        print("{} is in use with CNAME {}".format(subdomain, cname))
        
        # Check if the CNAME points to a service provider
        if any(sp in cname for sp in service_providers):
            print("Potential subdomain takeover vulnerability found: {} points to a service provider".format(subdomain))
            
            # Check if the service provider has a vulnerable subdomain takeover endpoint
            if service == "aws":
                response = requests.get("http://{}.s3.amazonaws.com".format(subdomain))
                if response.status_code == 404:
                    print("Takeover not possible")
                elif response.status_code == 403:
                    print("Access denied, potential takeover vulnerability found")
                elif response.status_code == 200:
                    print("Potential takeover vulnerability found")
            
            # Add checks for other service providers as needed
            
        else:
            print("{} is in use, but does not point to a service provider".format(subdomain))
            
    # Subdomain not in use
    except dns.resolver.NXDOMAIN:
        print("{} is available for takeover".format(subdomain))
