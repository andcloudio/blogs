# Asset Visibility and Access Policy Monitoring with Forseti

Cloud provides the ability for users to create resources with just few clicks. This can get out of control quickly without visibility into asset inventory, asset change history and monitoring of access controls. 

Forseti Security is a open source security tool which provides visibility and monitoring of GCP resources to ensure that access controls are set as intended and protected against unsafe changes.

![Alt text](img/forseti-gcp.png?raw=true "forseti")

Forseti security modules are 

- Inventory 

- Scanner 

- Enforcer 

- Explain 

- Notifier

## Inventory 

Inventory saves an inventory snapshot into Cloud SQL. This provides historical view of of what was in your cloud. With this, you can understand all the resources you have in GCP and take action to conserve resources, reduce costs, and minimize security exposure.

Inventory can be configured to run as often as you want, and send email notifications when there is an update.

## Scanner 

Scanner uses the information collected by the Forseti Inventory to regularly compare policy files that define the desired state of the resource against the current state of the resource.

## Enforcer

If it finds any differences in policy, Forseti Enforcer makes changes using Google Cloud APIs. 

## Explain

Explain can help you understand who has access to what resources, and how that user can interact with the resource, why a user has a permission on a resource, or why they don't have a permission, and how to fix it, what rules grant them permission, and which rules aren't in sync with recent changes. 

## Notifier

Notifier can dispatch notifications through various channels including Email, Slack, and Cloud Storage.

## Simple deployment of Forseti Security

Follow gives steps deployment of Forseti Security

https://cloud.google.com/community/tutorials/private-forseti-with-scc-integration

By default scanner job runs every 2 hours, if you dont want to wait then run scanner manually.

SSH to connect to the Forseti server VM: forseti-server-vm.

```bash
MODEL_ID=$(/bin/date -u +%Y%m%dT%H%M%S)

# Create an inventory
forseti inventory create --import_as ${MODEL_ID}

# select data model
forseti model use ${MODEL_ID}

# Run Forseti Scanner
forseti scanner run

# Run Forseti Notifier
forseti notifier run
```
or use script

```bash
home/ubuntu/forseti-security/install/gcp/scripts/run_forseti.sh
```

Forseti Scanner has default rules that create a violation when their conditions are met. Default rules can be found at gs://forseti-server-[ID]/rules

For example:

firewall_rules.yaml has rule

```yaml
rules:
  - rule_id: 'prevent_allow_all_ingress'
    description: Detect allow ingress to all policies
    mode: blacklist
    match_policies:
      - direction: ingress
        allowed: ['*']
    verify_policies:
      - allowed:
        - IPProtocol: 'all'
```

To test create a firewall rule to allow all ingress traffic

```bash
gcloud compute firewall-rules create test \
--priority 1000 \
--direction INGRESS \
--action allow \
--source-ranges 0.0.0.0/0 \
--rules all
```
on Security Command Center Findings we see FIREWALL_BLACKLIST_VIOLATION

![Alt text](img/forseti.png?raw=true "forseti")


We can add new rules and develop custom rules. Forseti has extensible architecture.

Summary:
Visibility and Control are essential when managing cloud deployments. 
Forseti security is one of security tool that should be there in your GCP environment. 
