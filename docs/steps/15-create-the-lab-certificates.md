**Step 15 — Create the lab certificates**

On **RHEL**:

```
sudo -i
```

Create a protected working folder:

```
umask 077

mkdir -p /root/siem-lab-pki

cd /root/siem-lab-pki
```

If this folder contains a working CA, preserve it and use it to issue the updated server certificate.

For a new CA:

```
openssl req -x509 -newkey rsa:3072 -sha256 -days 1825 \
  -keyout ca.key \
  -out ca.pem \
  -subj '/CN=SIEM Lab Root CA' \
  -addext 'basicConstraints=critical,CA:TRUE' \
  -addext 'keyUsage=critical,keyCertSign,cRLSign'
```

Enter a strong passphrase.

Create the server request:

```
openssl req -new -newkey rsa:3072 -noenc \
  -keyout splunk01.key \
  -out splunk01.csr \
  -subj '/CN=splunk01.lab.test'
```

Create the certificate settings:

```
cat > splunk01.ext <<'EOF'
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
subjectAltName=DNS:splunk01.lab.test,DNS:splunk01,IP:172.25.250.10
EOF
```

Sign the server certificate:

```
openssl x509 -req \
  -in splunk01.csr \
  -CA ca.pem \
  -CAkey ca.key \
  -CAcreateserial \
  -out splunk01.crt \
  -days 365 \
  -sha256 \
  -extfile splunk01.ext
```

Create and verify the files:

```
cat splunk01.crt splunk01.key ca.pem > splunk01.pem

cat splunk01.crt ca.pem > fullchain.pem

openssl x509 -in ca.pem -outform DER -out ca.cer

openssl verify -CAfile ca.pem splunk01.crt

openssl x509 -in splunk01.crt -noout -dates -ext subjectAltName
```

Install them:

```
install -d -o splunk -g splunk -m 700 /opt/splunk/etc/auth/lab

install -o splunk -g splunk -m 600 \
  splunk01.pem splunk01.key fullchain.pem ca.pem \
  /opt/splunk/etc/auth/lab/
```

Prepare only the public CA files for transfer:

```
install -d -m 755 /home/labadmin/siem-public

install -m 644 ca.pem ca.cer /home/labadmin/siem-public/

sha256sum \
  /home/labadmin/siem-public/ca.pem \
  /home/labadmin/siem-public/ca.cer

exit
```

**Command overview:**

| Command or option   | Explanation                               |
| ------------------- | ----------------------------------------- |
| `sudo -i`           | Opens an administrator shell.             |
| `umask 077`         | Makes new files private.                  |
| `openssl req -x509` | Creates the CA certificate.               |
| `-newkey rsa:3072`  | Creates an RSA key.                       |
| `-days`             | Sets certificate lifetime.                |
| `openssl req -new`  | Creates the server’s signing request.     |
| `-noenc`            | Allows unattended service startup.        |
| `subjectAltName`    | Lists valid names and the server address. |
| `openssl verify`    | Checks the certificate chain.             |
| `install -m 600`    | Restricts private-file access.            |
| `exit`              | Returns to `labadmin`.                    |

Keep private keys outside the project. Renew the server certificate before its one-year expiry.

Splunk supports custom certificates for forwarding and browser connections. [help.splunk.com](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/secure-splunk-platform-communications-with-transport-layer-security-certificates/configure-splunk-indexing-and-forwarding-to-use-tls-certificates?utm_source=chatgpt.com)

---
