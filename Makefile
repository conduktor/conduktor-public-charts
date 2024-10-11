# Global Vars
#############

WORKING_DIR 	 = $(shell pwd)
OS 				 = $(shell uname -s)
ARCH 			 = $(shell uname -m)
NAMESPACE 		 = conduktor
TEST_NAMESPACE 	 = ct
K3D_CONTEXT_NAME = k3d-conduktor-platform

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

.PHONY: install-githooks
install-githooks: ## Install git hooks
	git config --local core.hooksPath .githooks

.PHONY: install-readme-generator
install-readme-generator: ## Install bitnami/readme-generator-for-helm using NMP
	@echo "Check that NPM is installed"
	command -v npm || echo -e "Missing NPM"; exit 1;
	@echo "Install readme-generator"
	npm install -g @bitnami/readme-generator-for-helm@2.6.1


.PHONY: generate-readme
generate-readme: ## Re-generate cgharts README
	@echo "Check that readme-generator is installed"
	command -v readme-generator || $(MAKE) install-readme-generator
	
	@echo
	@echo "Updating README.md for console chart"
	readme-generator --values "./charts/console/values.yaml" --readme "./charts/console/README.md"

	@echo
	@echo "Updating README.md for gateway chart"
	readme-generator --values "./charts/gateway/values.yaml" --readme "./charts/gateway/README.md"


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
	mkdir ~/.k3d || true

	@echo "Create the test cluster"
	k3d cluster create --config $(CURDIR)/k3d/config.yaml

	@echo "Current context : $$(kubectl config current-context)"

.PHONY: check-kube-context
check-kube-context: ## Validate that current kube context used is K3D to prevent installing chart on another cluster
	@if [ "$$(kubectl config current-context)" != "$(K3D_CONTEXT_NAME)" ]; then \
		echo -e "Current context is not K3D cluster ! ($$(kubectl config current-context))"; \
		exit 1; \
	fi

.PHONY: delete-k3d-cluster
delete-k3d-cluster: ## Delete k3d cluster
	make check-kube-context
	@echo "Deleting k3d cluster"
	k3d cluster delete --config $(CURDIR)/k3d/config.yaml || true

.PHONY: helm-nginx
helm-nginx: ## Install nginx-ingress helm chart from ingress-nginx
	make check-kube-context

	@echo "Installing nginx-ingress"
	helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
	  --namespace ingress-nginx --create-namespace
	@echo "Waiting for ingress-nginx to be ready..."
	kubectl wait deployment -n ingress-nginx \
		ingress-nginx-controller --for condition=Available=True --timeout=90s

.PHONY: helm-postgresql
helm-postgresql: ## Install postgresql helm chart from bitnami
	make check-kube-context
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
	make check-kube-context
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
.ONESHELL:
helm-monitoring-stack: ## Install monitoring stack prometheus and grafana
	make check-kube-context
	@echo "Add prometheus helm repo"
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts || true
	helm repo update
	@echo "Install prometheus stack"
	helm upgrade --install prometheus-stack prometheus-community/kube-prometheus-stack \
		--namespace prometheus-stack --create-namespace \
		--set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false \
		--set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
		--set alertmanager.enabled=false \
		--set grafana.enabled=false
	@echo "Install grafana operator"
	helm upgrade --install grafana-operator bitnami/grafana-operator \
		--namespace prometheus-stack --create-namespace \
		--set namespaceScope=false \
		--set watchNamespaces="" \
		--set grafana.enabled=false
	@echo "Install grafana"
	kubectl apply -f k3d/monitoring-stack-grafana-crd.yaml

.PHONY: create-test-ns
create-test-ns: ## Create test namespace
	make check-kube-context
	kubectl create namespace ${TEST_NAMESPACE} || true

.PHONY: test-chart
test-chart: ## Run chart-testing 
	make check-kube-context
	make create-test-ns
	ct install --config $(CURDIR)/.github/ct-config.yaml
