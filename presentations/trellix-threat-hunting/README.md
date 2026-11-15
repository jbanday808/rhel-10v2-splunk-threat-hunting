# Trellix Cyber Threat Hunter / Consultant

This guide helps you explain the role to someone without a cybersecurity background. Use it alongside the [Trellix customer PowerPoint](Trellix_Customer_Product_Brief.pptx). Download the file from GitHub and open it in PowerPoint or another compatible presentation app.

The 56-slide deck introduces a broad range of Trellix products. Its examples are illustrations, and available features depend on the customer's products, configuration and agreement. Confirm current names, licensing and supported systems with Trellix before making a recommendation.

## The role in everyday language

A cyber threat hunter looks for signs that an intruder may have entered an organization's systems, even when no clear alarm has sounded. A consultant works with the customer to decide what to examine, explains the findings, and helps the customer choose practical next steps.

The work starts with a question and permission to investigate. The hunter looks at the information available from computers, accounts and networks, checks whether unusual activity has an ordinary explanation, and reports what the evidence supports. The customer and its authorized responders decide which changes or response actions to approve.

**A simple introduction:**

> “My job is to help your team look for signs of hidden cyber threats. We agree on the question and the systems to review, investigate the available clues, and explain what we found in terms your team can act on.”

## A short route through the PowerPoint

You do not need to show every slide. For a 10–15 minute introduction, select the slides that fit the customer's concern.

| Slides | Topic | What to say |
| --- | --- | --- |
| 2–3 | Executive summary | “Let's start with the business concern and the outcome you want to improve.” |
| 7–10 | Device investigation | “These tools can help a security team examine suspicious activity on computers and collect evidence.” |
| 21 and 24 | Network activity | “Looking at connections between systems can add context to what happened on a device.” |
| 25–26 | Threat intelligence and SecondSight | “Threat information helps focus the search. SecondSight adds Trellix specialists to the hunt.” |
| 35 and 40–41 | Joining the clues | “An email, a device alert and network activity may be related. The team checks the evidence before reaching a conclusion.” |
| 42–44 | Customer questions | “What do you need to protect, what tools do you already use, and where does your team need help?” |
| 50–52 | Next steps and example evaluation | “Agree on a small test, who is responsible, and how you will judge the outcome.” |

The deck's speaker notes provide additional talking points in a compatible presentation app. Slides 53–55 list additional product documentation and may include older or separately managed components.

Use the [customer threat-hunt evaluation worksheet](CUSTOMER_HUNT_EVALUATION_WORKSHEET.md) to turn the questions on slides 42–44 and the example evaluation on slides 50–52 into an agreed scope, evidence check, success measure, and next decision. Keep any completed customer copy private.

## Example conversation: an unusual sign-in

Imagine the customer asks whether an employee account was misused. Several failed sign-ins are followed by a successful sign-in. That pattern can have an innocent explanation, such as a forgotten password, or it may need investigation.

1. **Agree on the scope:** Ask which account and time period may be reviewed, who owns the decision, and what information is available.
2. **Review the clues:** With permission, compare sign-in records with device activity and information the customer can verify.
3. **Explain the result:** Describe the observed activity, possible explanations, and any missing information. Do not call it an attack without supporting evidence.
4. **Discuss next steps:** If the evidence warrants it, ask the customer's authorized team to review account access and decide whether additional protection or response is needed.

An example briefing: “We saw several unsuccessful sign-ins followed by a successful one. We have not yet established whether the successful sign-in was authorized. The account owner should confirm the activity before we draw a conclusion.”

## Where syslog helps

The role calls for configuring and reviewing operating-system and application logs. Syslog is one way to collect those records. In the [syslog practice guide](../../docs/security-operations/SYSLOG_HUNTING_GUIDE.md), the RHEL lab records a harmless test message, Splunk makes it searchable, and the hunter checks sign-in clues before explaining what they mean. This demonstrates the logging and analysis workflow; it does not connect Trellix products to the lab.

## Useful words

| Term | Plain-language meaning |
| --- | --- |
| Endpoint | A computer, server, phone or other device connected to a network. |
| EDR | Endpoint detection and response: tools that help investigate suspicious activity on devices. |
| Threat intelligence | Information about threats that helps a team decide what to investigate. |
| Evidence | Records or observations that support a finding. A clue alone may have several explanations. |
| Threat hunt | A planned search for signs of suspicious activity. |
| Syslog | A way for a system or application to record an activity message for review. |
| Proof of concept | A small, agreed test used to see whether an approach meets the customer's needs. |

## Further reading

- [Trellix SecondSight](https://www.trellix.com/products/secondsight/) describes Trellix's managed threat-hunting service.
- [Trellix EDR documentation](https://docs.trellix.com/v1/docs/endpoint-detection-and-response-edr) describes device investigation and hunting capabilities.
- [Trellix product portfolio](https://www.trellix.com/products/) is the starting point for current product information.
- [Hunt planning template](../../docs/security-operations/templates/threat-hunt-plan.md) and [hunt briefing template](../../docs/security-operations/templates/hunt-briefing.md) help turn the conversation into a documented engagement.

This is an educational guide for the role, not a claim that the lab has a working Trellix deployment or that a particular customer engagement has taken place.
