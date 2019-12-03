# AWS resource cleanup tools

## cloud-nuke

- An open source tool that can delete all the resources in your cloud environment. 

- The key feature is the ability to delete all resources older than a certain age.

- run cloud-nuke as a cron job once per day in each sandbox environment to delete all resources that are more than two days old

    $ cloud-nuke aws --older-than 48h

## Janitor Monkey

- cleans up AWS resources on a configurable schedule, default is once per week

- ability to send a notification to the owner of the resource a few days before deletion.

- Chaos Monkey, a tool for testing application resiliency. 

## aws-nuke

- An open source tool dedicated to deleting everything in an AWS account. 
