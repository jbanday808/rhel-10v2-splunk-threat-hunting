# HTTP Event Collector setup

Follow the HEC appendix. `inputs.conf.example` contains global TLS settings to merge into the existing `[http]` stanza on the Splunk server. It is not an automatically deployed app and contains no token. Keep the real `splunk_httpinput/local/inputs.conf`, HEC tokens, and backups outside the repository.

Create the dedicated token in Splunk Web, permit only the `lab` index, choose `siem:hec`, and leave indexer acknowledgment off for the simple test. Review the TLS certificate and effective global settings, restart if needed, then run `bash scripts/rhel/send-hec-event.sh` as labadmin.

The sender prompts without echo, keeps the authorization header in a temporary private file, and removes it on exit. Do not trace the sender with `bash -x`. It sends one event without automatic retries because repeating a request can create duplicates. A successful HEC response still requires a Splunk search for the exact printed ID.
