**Step 30 — Create the dashboard and analyst role**

On **RHEL**, create the dashboard:

```
cat > apps/LAB_SIEM/default/data/ui/views/overview.xml <<'EOF'
<dashboard version="1.1">
  <label>Threat Hunting Lab Overview</label>
  <description>Lab activity during the last 24 hours.</description>

  <row>
    <panel>
      <title>Events by index</title>
      <chart>
        <search>
          <query>(index=win_security OR index=win_system OR index=powershell OR index=sysmon OR index=linux OR index=lab) | stats count by index</query>
          <earliest>-24h</earliest>
          <latest>now</latest>
        </search>
        <option name="charting.chart">column</option>
      </chart>
    </panel>
  </row>

  <row>
    <panel>
      <title>Recent process starts</title>
      <table>
        <search>
          <query>index=sysmon EventCode=1 | table _time host User Image ParentImage CommandLine | head 50</query>
          <earliest>-24h</earliest>
          <latest>now</latest>
        </search>
      </table>
    </panel>
  </row>
</dashboard>
EOF
```

Create the role:

```
cat > apps/LAB_SIEM/local/authorize.conf <<'EOF'
[role_lab_hunter]
search = enabled
get_metadata = enabled
get_typeahead = enabled
change_own_password = enabled
srchIndexesAllowed = win_security;win_system;powershell;sysmon;linux;lab
srchIndexesDefault = win_security;win_system;powershell;sysmon;linux;lab
srchJobsQuota = 3
EOF
```

Create permissions:

```
cat > apps/LAB_SIEM/metadata/default.meta <<'EOF'
[]
access = read : [ admin, lab_hunter ], write : [ admin ]
export = system
EOF
```

Deploy the updated app:

```
sudo cp -a apps/LAB_SIEM/. /opt/splunk/etc/apps/LAB_SIEM/

sudo chown -R splunk:splunk /opt/splunk/etc/apps/LAB_SIEM

sudo find /opt/splunk/etc/apps/LAB_SIEM \
  -type d -exec chmod 750 {} +

sudo find /opt/splunk/etc/apps/LAB_SIEM \
  -type f -exec chmod 640 {} +

sudo -u splunk /opt/splunk/bin/splunk btool check

sudo systemctl restart Splunkd
```

In Splunk:

1. Open the **Threat Hunting Lab** app.
2. Open its Overview dashboard.
3. Create a separate analyst account.
4. Assign only `lab_hunter` for the access test.
5. Confirm it can search the six lab indexes.
6. Confirm it cannot retrieve protected `_internal` records.

**File overview:** The role permits lab searches and allows users to change their own passwords. Administrators retain configuration access.

---
