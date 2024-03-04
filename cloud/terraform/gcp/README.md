# Create a VM on GCP using Terraform

## Create the variables file `terraform.tfvars`

```
gcp_project = < The name of your GCP project >
gcp_region = < The region to provision the VM >
ssh_public_key = < SSH Public key to inject into the VM >
service_account = < The email address of the Service Account created earlier >
```

## Initialize Terraform

```bash
terraform init
```

## Provision the environment

```bash
terraform apply
```

## Destroy the environment

```bash
terraform destory
```
