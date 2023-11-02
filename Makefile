# Global Vars
#############

WORKING_DIR 	= $(shell pwd)
OS 				= $(shell uname -s)
ARCH 			= $(shell uname -m)
NAMESPACE 		= conduktor
TEST_NAMESPACE 	= ct

# Helm dependencies specific default variables
##############################################

postgresql_password := conduktor
postgresql_default_database := conduktor
minio_password := conduktor
minio_default_bucket := conduktor

# Main targets you should run
#############################
.DEFAULT_GOAL := help

.PHONY: help
help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: helm-deps
helm-deps: ## Install helm dependencies
	@echo "Installing helm dependencies"
	helm repo add conduktor https://helm.conduktor.io/ || true
	helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx || true
	helm repo add bitnami https://charts.bitnami.com/bitnami || true
	helm repo update

.PHONY: k3d-up
k3d-up: ## Setup k3d cluster
	@echo "Creating k3d cluster"
	make create-k3d-cluster
	@echo "Installing nginx-ingress"
	make helm-nginx
	@echo "Installing postgresql"
	make helm-postgresql
	@echo "Installing Minio"
	make helm-minio
	@echo "Create Test namespace"
	make create-test-ns

.PHONY: k3d-ci-up
k3d-ci-up: ## Setup CI k3d cluster
	@echo "Creating k3d cluster"
	make create-k3d-cluster
	@echo "Installing nginx-ingress"
	make helm-nginx
	@echo "Create Test namespace"
	make create-test-ns

.PHONY: k3d-down
k3d-down: ## Teardown k3d cluster
	make delete-k3d-cluster

# Extended targets
##################

.PHONY: create-k3d-cluster
create-k3d-cluster: ## Create k3d cluster
	@echo "Creating k3d directory if not existing"
	mkdir .k3d || true
	@echo "Create the test cluster"
	k3d cluster create -p "80:80@loadbalancer" \
		--k3s-arg '--disable=traefik@server:0' \
		--wait \
		--k3s-arg '--kubelet-arg=eviction-hard=imagefs.available<1%,nodefs.available<1%@agent:*' \
        --k3s-arg '--kubelet-arg=eviction-minimum-reclaim=imagefs.available=1%,nodefs.available=1%@agent:*' \
        --k3s-arg '--kubelet-arg=eviction-hard=imagefs.available<1%,nodefs.available<1%@server:0' \
        --k3s-arg '--kubelet-arg=eviction-minimum-reclaim=imagefs.available=1%,nodefs.available=1%@server:0' \
        --kubeconfig-switch-context=true \
        --kubeconfig-update-default=true \
        conduktor-platform
	@echo "Add kubeconfig to .k3d/kubeconfig.yml"
	k3d kubeconfig get conduktor-platform > .k3d/kubeconfig.yml
	# k3d create a kubeconfig with host `0.0.0.0`, it's a problem as
	# cluster certificate only got DSN for `localhost`
	@if [ "${UNAME_S}" = "Linux" ]; then \
		sed -i "s/0\.0\.0\.0/localhost/g" ./.k3d/kubeconfig.yml; \
    fi
	@if [ "${UNAME_S}" = "Darwin" ]; then \
  		sed -i -e "s/0\.0\.0\.0/localhost/" .k3d/kubeconfig.yml; \
    fi

.PHONY: delete-k3d-cluster
delete-k3d-cluster: ## Delete k3d cluster
	@echo "Deleting k3d cluster"
	k3d cluster delete conduktor-platform || true
	rm -rf .k3d || true

.PHONY: helm-nginx
helm-nginx: ## Install nginx-ingress helm chart from ingress-nginx
	@echo "Installing nginx-ingress"
	helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
	  --namespace ingress-nginx --create-namespace
	@echo "Waiting for ingress-nginx to be ready..."
	kubectl wait deployment -n ingress-nginx \
		ingress-nginx-controller --for condition=Available=True --timeout=90s

.PHONY: helm-postgresql
helm-postgresql: ## Install postgresql helm chart from bitnami
	kubectl create namespace ${NAMESPACE} || true
	@echo "Installing postgresql"
	helm upgrade --install postgresql bitnami/postgresql \
		--namespace ${NAMESPACE} --create-namespace \
		--version 12.5.8 \
		--set global.postgresql.auth.database=${postgresql_default_database} \
		--set global.postgresql.auth.postgresPassword=${postgresql_password} \
		--set auth.postgresPassword=${postgresql_password} \
		--set primary.service.type=LoadBalancer
	@echo "Waiting for postgresql to be ready..."
	kubectl rollout status --watch --timeout=300s statefulset/postgresql -n ${NAMESPACE}


.PHONY: helm-minio
helm-minio: ## Install minio helm chart from bitnami
	kubectl create namespace ${NAMESPACE} || true
	@echo "Installing Minio"
	helm upgrade --install minio bitnami/minio \
		--namespace ${NAMESPACE} --create-namespace \
		--version 12.8.0 \
	    --set auth.rootPassword=${minio_password} \
	    --set defaultBuckets=${minio_default_bucket} \
	    --set disableWebUI=false
	@echo "Waiting for minio to be ready..."
	kubectl rollout status --watch --timeout=300s deployment/minio -n ${NAMESPACE}

.PHONY: helm-monitoring-stack
helm-monitoring-stack: ## Install monitoring stack prometheus and grafana
	@echo "Add prometheus helm repo"
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts || true
	helm repo update
	@echo "Install prometheus stack"
	helm upgrade --install prometheus-stack prometheus-community/kube-prometheus-stack \
		--namespace prometheus-stack --create-namespace \
		--set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false \
		--set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
		--set alertmanager.enabled=false \
		--set grafana.enabled=true


.PHONY: create-test-ns
create-test-ns: ## Create test namespace
	kubectl create namespace ${TEST_NAMESPACE} || true
