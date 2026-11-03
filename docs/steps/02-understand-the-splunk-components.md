**Step 2 — Understand the Splunk components**

| Component                                        | Simple explanation                                               | Placement                                          |
| ------------------------------------------------ | ---------------------------------------------------------------- | -------------------------------------------------- |
| **Indexer**                                      | Receives and stores records so you can search them later.        | RHEL                                               |
| **Universal Forwarder**                          | Collects records from a computer and sends them to Splunk.       | Windows VM                                         |
| **Heavy Forwarder**                              | Can organize or filter records before sending them onward.       | Optional future RHEL VM                            |
| **Search Head**                                  | Provides searches, dashboards, reports, and alerts.              | Same RHEL server                                   |
| **Search Peer**                                  | Searches its stored records when another Search Head asks it to. | Used when you separate the Search Head and indexer |
| **Deployment Server**                            | Distributes settings and apps to forwarders.                     | Optional future expansion                          |
| **License Manager**, formerly **License Master** | Coordinates Splunk license use across servers.                   | This standalone server uses its local license      |

A Universal Forwarder does not provide full indexing and searching. A Deployment Server distributes configuration; it does not carry the endpoint’s event traffic. [help.splunk.com](https://help.splunk.com/en/splunk-enterprise/forward-and-process-data/forwarding-and-receiving-data/10.4/introduction-to-forwarding/types-of-forwarders?utm_source=chatgpt.com)

This updated guide builds **three VMs**: a RHEL Splunk server, a Windows hunting endpoint, and a separate RHEL IdM directory server. LDAP sign-in is configured on the Splunk search interface; additional Splunk Enterprise roles would also run on RHEL if you expand the lab.

---
