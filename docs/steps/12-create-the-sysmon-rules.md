**Step 12 — Create the Sysmon rules**

On **RHEL**:

```
cat > sysmon/sysmon.xml <<'EOF'
<Sysmon schemaversion="4.82">
  <HashAlgorithms>SHA256</HashAlgorithms>
  <EventFiltering>
    <ProcessCreate onmatch="exclude" />

    <NetworkConnect onmatch="include">
      <Image condition="end with">powershell.exe</Image>
      <Image condition="end with">curl.exe</Image>
    </NetworkConnect>

    <FileCreate onmatch="include">
      <TargetFilename condition="begin with">C:\SIEMLab\TestFiles\</TargetFilename>
    </FileCreate>

    <RegistryEvent onmatch="include">
      <TargetObject condition="contains">\CurrentVersion\Run\SIEMLab</TargetObject>
    </RegistryEvent>

    <DnsQuery onmatch="include">
      <Image condition="end with">powershell.exe</Image>
    </DnsQuery>
  </EventFiltering>
</Sysmon>
EOF
```

**File overview:** This records process starts and selected network, file, registry, and DNS activity.

The empty process exclusion records all process starts. The other rules limit selected event types for the lab. [learn.microsoft.com](https://learn.microsoft.com/sysinternals/downloads/sysmon?utm_source=chatgpt.com)

---
