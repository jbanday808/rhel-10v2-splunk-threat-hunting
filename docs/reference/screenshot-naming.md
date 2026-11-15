# Screenshot names and captions

Save approved images under [`screenshots/`](../../screenshots/), not `docs/images/`. The [screenshot index](../../screenshots/README.md) describes the images already in the repository. Keep existing filenames and links unless you are deliberately replacing an image and have checked every reference.

## Choose a name

| Image group | Current pattern | Example already in the repository |
| --- | --- | --- |
| Lab setup and logging | Two-digit number, underscore, short description, `.png` | [`18_Rsyslog_SIEM_Lab_Config.png`](../../screenshots/18_Rsyslog_SIEM_Lab_Config.png) |
| Earlier network-analysis workbench | Two-digit number, hyphen, short description, `.jpg` | [`02-tool-library.jpg`](../../screenshots/network-defense-lab/02-tool-library.jpg) |

For a new hunting image, choose the relevant group under `screenshots/`, use its existing naming pattern, and continue the sequence within that group. Use a short description of what the image shows. Do not put a real username, address, token, or customer name in the filename. The nine obsolete TraceVector interface captures were removed; capture new views only after checking the current Site.

## Review before publishing

1. Confirm the capture comes from your owned lab or another source you are authorized to share.
2. Crop or obscure credentials, private identifiers, browser sessions, and unrelated content. Check the final image itself, including visible tabs and notifications.
3. Write one sentence describing **only what is visible**. For example, a configuration screenshot can show a setting, but it cannot prove that events reached Splunk.
4. Add the reviewed image to [`screenshots/`](../../screenshots/) and link it from the relevant guide or screenshot index. Open the link to make sure it resolves.

Keep raw captures and private evidence outside Git. Follow the [public repository publication checklist](security-and-sanitization.md) before committing any image. Record live test results separately, with the time, system, method, and observed result.
