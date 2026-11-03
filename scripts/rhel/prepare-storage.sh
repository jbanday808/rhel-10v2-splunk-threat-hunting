#!/usr/bin/env bash
set -euo pipefail

[[ $EUID -eq 0 ]] || {
  echo 'Run with sudo.' >&2
  exit 1
}

DISK=$(readlink -f "${1:?Provide the new blank data disk}")

[[ -b "$DISK" ]] || {
  echo 'Not a block device.' >&2
  exit 1
}

[[ $(lsblk -dn -o TYPE "$DISK") == disk ]] || {
  echo 'Select a whole disk.' >&2
  exit 1
}

[[ $(lsblk -nr -o NAME "$DISK" | wc -l) -eq 1 ]] || {
  echo 'Disk has child devices; stopping.' >&2
  exit 1
}

[[ -z $(lsblk -n -o MOUNTPOINTS "$DISK") ]] || {
  echo 'Disk is mounted; stopping.' >&2
  exit 1
}

SIGNATURES=$(wipefs -n --noheadings "$DISK")

[[ -z "$SIGNATURES" ]] || {
  echo 'Disk has existing signatures; stopping.' >&2
  exit 1
}

if findmnt --mountpoint /splunkdata >/dev/null ||
   grep -Eq '[[:space:]]/splunkdata[[:space:]]' /etc/fstab; then
  echo '/splunkdata is already configured; stopping.' >&2
  exit 1
fi

lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS "$DISK"

read -r -p "Type the full disk path ($DISK) to initialize it: " ANSWER
[[ "$ANSWER" == "$DISK" ]] || exit 1

parted --script "$DISK" mklabel gpt
parted --script "$DISK" mkpart primary xfs 1MiB 100%
partprobe "$DISK"
udevadm settle

PARTITION=$(lsblk -lnpo NAME,TYPE "$DISK" |
  awk '$2 == "part" {print $1; exit}')

[[ -b "$PARTITION" ]] || exit 1

mkfs.xfs -L SIEMDATA "$PARTITION"

mkdir -p /splunkdata

DATA_UUID=$(blkid -s UUID -o value "$PARTITION")

cp -a /etc/fstab "/etc/fstab.before-siem-$(date +%Y%m%dT%H%M%S)"

printf 'UUID=%s /splunkdata xfs defaults 0 0\n' "$DATA_UUID" >> /etc/fstab

systemctl daemon-reload
mount /splunkdata

chown splunk:splunk /splunkdata
chmod 750 /splunkdata

findmnt --mountpoint /splunkdata
df -h /splunkdata
