Place your TLS certificate and private key in this folder:
- server.crt
- server.key

For local testing, you can generate a self-signed certificate:

```bash
openssl req -x509 -newkey rsa:4096 -nodes -keyout server.key -out server.crt -days 365 -subj "/CN=localhost"
```
