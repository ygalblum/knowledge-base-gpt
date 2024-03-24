# Deploy Ollama on the remote machine

## Install the ollama collection
```bash
ansible-galaxy collection install ygalblum.ollama
```

## Create your environment file
The [settings.yml](./settings.yml) includes the basic settings required by the application.
The only missing configuration is that of the certificate.

For Kubernetes Certificate Manager based certificate:
```yaml
ollama_use_k8s_cert_manager: true
ollama_certificate_namespace: < Namespace of the Certificate Issuer >
ollama_certificate_ca_issuer: < Name of the Certificate Issuer >
ollama_fqdn: < FQDN of the remote VM >
```

## Create the Inventory file
```yaml
all:
  hosts:
  children:
    ollama:
      hosts:
        < FQDN of the remote VM >:
```

## Run the installer
```bash
ansible-playbook -i </path/to/inventory> -e @</path/to/env_file> -e @settings.yml ygalblum.ollama.install
```
