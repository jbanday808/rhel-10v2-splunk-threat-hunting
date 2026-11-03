# Dummy password test cases

All values in `cases.json` are fake fixture tokens. They demonstrate only the supported unquoted token grammar. They are not observed Splunk events or real credentials.

Run `python3 -B -m unittest discover -s tests -p 'test_*.py' -v` from the project root. The tests read the shipped `SEDCMD-redact_pw` expression and exercise its substitution using Python's regular expression engine. These shared regex features provide an offline check; Splunk's live parser must still be validated using the appendix and a fresh dummy record.
