**Step 7 — Register, update, and prepare RHEL**

If not already registered:

```
sudo subscription-manager register
```

Then:

```
sudo subscription-manager identity

sudo subscription-manager repos --list-enabled

sudo subscription-manager release --list
```

If `10.2` appears in the release list:

```
sudo subscription-manager release --set=10.2
```

Resolve any registration or release-selection problem before continuing.

Install updates and tools:

```
sudo dnf upgrade --refresh -y

sudo dnf install -y \
  chrony firewalld openssl tar gzip curl \
  openssh-server openssh-clients \
  rsyslog logrotate audit acl parted xfsprogs \
  util-linux policycoreutils policycoreutils-python-utils \
  procps-ng python3 open-vm-tools
```

Enable services:

```
sudo systemctl enable --now \
  chronyd firewalld rsyslog sshd vmtoolsd

sudo timedatectl set-timezone UTC

chronyc tracking

chronyc sources -v

sudo reboot
```

**Command overview:**

| Command                  | Explanation                                    |
| ------------------------ | ---------------------------------------------- |
| `subscription-manager`   | Manages registration and software access.      |
| `dnf upgrade`            | Installs updates.                              |
| `dnf install`            | Installs the named tools.                      |
| `systemctl enable --now` | Starts services and enables automatic startup. |
| `timedatectl`            | Sets the time zone.                            |
| `chronyc`                | Checks clock synchronization.                  |
| `reboot`                 | Restarts RHEL.                                 |

After restarting:

```
cat /etc/redhat-release

getenforce

df -h /
```

Confirm RHEL 10.2, SELinux `Enforcing`, and sufficient free space.

---
