# infrastructure code workflows

## Use version control

- git clone

- live and modules repos

- Don’t use branches

## Run the code locally

- Run in a sandbox environment

- terraform apply

- go test

## Make code changes

- Change the code

- terraform apply

- go test

- Use test stages

## Submit changes for review

- Submit a pull request

- Enforce coding guidelines

## Run automated tests

- Tests run on CI server

- Unit tests

- Integration tests

- End-to-end tests

- Static analysis

- terraform plan

## Merge and release

- git tag

- Use repo with tag as versioned, immutable artifact

## Deploy

- Deploy with Terraform, Atlantis, Terraform Enterprise, Terragrunt, scripts

- Limited deployment strategies. Make sure to handle errors: retries errored.tfstate!

- Run deployment on a CI server

- Give CI server admin permissions

- Promote immutable, versioned artifacts across environments

