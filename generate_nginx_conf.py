template_with_SSL = '''
# HTTP Server - Redirect all requests to HTTPS
server {
    listen 80;
    server_name transportation.games;
    
    # Redirect all HTTP requests to HTTPS
    return 301 https://$host$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl;
    server_name {};

    # SSL Configuration - Replace with your cert and private key
    ssl_certificate {};
    ssl_certificate_key {};

    # Proxy settings
    location / {
        proxy_pass https://localhost:{};
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
'''

template_without_SSL = '''
# HTTP Server - Redirect all requests to HTTPS
server {
    listen 80;
    server_name %s;
    
    location / {
        proxy_pass http://localhost:%d;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }   
}

'''

from argparse import ArgumentParser

if __name__ == "__main__":
    ps = ArgumentParser()
    ps.add_argument("--server-name", type=str, required=True)
    ps.add_argument("--local-service-port", type=int, required=True)
    ps.add_argument("--enable-ssl", type=lambda x : x in ['y', 'Y'], default=False)
    ps.add_argument("--ssl-cert", type=str)
    ps.add_argument("--ssl-key", type=str)
    
    args = ps.parse_args()
    
    if args.enable_ssl:
        if not all([args.ssl_cert, args.ssl_key]):
            print("Plase set --ssl-crt and --ssl-key")
        conf = template_with_SSL % (args.server_name, args.ssl_cert, args.ssl_key, args.local_service_port)
    else:
        conf = template_without_SSL % (args.server_name, args.local_service_port)
    with open("nginx.conf", "w") as f:
        f.write(conf)
        
    print("Generated nginx.conf")
    


