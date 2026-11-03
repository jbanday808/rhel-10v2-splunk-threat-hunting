**Step 9 — Understand the configuration files**

Use Splunk’s exact filenames: **`outputs.conf`** and **`transforms.conf`**.

| File              | Simple explanation                                    |
| ----------------- | ----------------------------------------------------- |
| `inputs.conf`     | Chooses records to collect or receive.                |
| `outputs.conf`    | Tells the collector where to send records.            |
| `props.conf`      | Tells Splunk how to read each entry.                  |
| `transforms.conf` | Defines rules for extracting useful details.          |
| `indexes.conf`    | Creates separate storage areas and sets their limits. |
| `authentication.conf` | Connects Splunk sign-in to the directory and maps groups to roles. |
| `authorize.conf` | Defines the actions and indexes each Splunk role can use. |
| `etc/openldap/ldap.conf` | Requires certificate checks for Splunk LDAP connections. |

These files manage different stages of collecting, reading, forwarding, and storing records. [help.splunk.com](https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.6/administer-splunk-enterprise-with-configuration-files/list-of-configuration-files?utm_source=chatgpt.com)

---
