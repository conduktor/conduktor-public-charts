# Global Vars
#############

WORKING_DIR 	     = $(shell pwd)
OS 				     = $(shell uname -s)
ARCH 			     = $(shell uname -m)
NAMESPACE 		     = conduktor
MONITORING_NAMESPACE = prometheus-stack
TEST_NAMESPACE 	     = ct
K3D_CONTEXT_NAME     = k3d-conduktor-platform

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
	npm install -g @bitnami/readme-generator-for-helm@2.7.0


.PHONY: generate-readme
generate-readme: ## Re-generate charts README
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

.PHONY: install-dev-deps
install-dev-deps:  ## Install development dependencies (PostgreSQL, Minio, monitoring stack) not needed for CT tests
	kubectl create namespace ${NAMESPACE} || true
	@echo "Installing postgresql"
	make helm-postgresql
	@echo "Installing Minio"
	make helm-minio
	@echo "Installing Monitoring stack"
	make helm-monitoring-stack
	@echo "Stack ready"
	@echo "Postgresql:"
	@echo "	Internal : postgresql.${NAMESPACE}.svc.cluster.local:5432"
	@echo "	Credentials : postgres/${postgresql_password} on database ${postgresql_default_database}"
	@echo "Minio:"
	@echo "	Internal : minio.${NAMESPACE}.svc.cluster.local:9001"
	@echo "	Port-Forward : $ kubectl port-forward svc/minio -n ${NAMESPACE} 9001:9001"
	@echo "	Credentials : admin/${minio_password}"
	@echo "Prometheus:"
	@echo "	Internal : prometheus-stack-kube-prom-prometheus.${MONITORING_NAMESPACE}.svc.cluster.local:9090"
	@echo "	Port-Forward : $ kubectl port-forward svc/prometheus-stack-kube-prom-prometheus -n ${MONITORING_NAMESPACE} 9090:9090"
	@echo "Grafana:"
	@echo "	Internal : grafana-service.${MONITORING_NAMESPACE}.svc.cluster.local:3000"
	@echo "	Access Grafana with : $ kubectl port-forward svc/grafana-service -n ${MONITORING_NAMESPACE} 3000:3000"
	@echo "	Credentials : admin/admin"

# Extended targets
##################

.PHONY: create-k3d-cluster
create-k3d-cluster: ## Create k3d cluster
	@echo "Create the test cluster"
	@if grep -q btrfs /proc/mounts; then \
		echo "Btrfs filesystem detected. Mounting /dev/mapper. See https://k3d.io/v5.8.3/faq/faq/"; \
		k3d cluster create --config $(CURDIR)/k3d/config.yaml -v /dev/mapper:/dev/mapper; \
	else \
		k3d cluster create --config $(CURDIR)/k3d/config.yaml; \
	fi
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
	@echo "Installing postgresql"
	helm upgrade --install postgresql bitnami/postgresql \
		--namespace ${NAMESPACE} --create-namespace \
		--version 12.5.8 \
		--set global.postgresql.auth.database=${postgresql_default_database} \
		--set global.postgresql.auth.postgresPassword=${postgresql_password} \
		--set auth.postgresPassword=${postgresql_password} \
		--set primary.service.type=LoadBalancer \
		--set primary.persistence.size=1Gi
	@echo "Waiting for postgresql to be ready..."
	kubectl rollout status --watch --timeout=300s statefulset/postgresql -n ${NAMESPACE}


.PHONY: helm-minio
helm-minio: ## Install minio helm chart from bitnami
	make check-kube-context
	@echo "Installing Minio"
	helm upgrade --install minio bitnami/minio \
		--namespace ${NAMESPACE} --create-namespace \
		--version 12.8.0 \
	    --set auth.rootPassword=${minio_password} \
	    --set defaultBuckets=${minio_default_bucket} \
	    --set disableWebUI=false \
	    --set persistence.size=1Gi
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
	helm upgrade --install ${MONITORING_NAMESPACE} prometheus-community/kube-prometheus-stack \
		--namespace ${MONITORING_NAMESPACE} --create-namespace \
		--set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false \
		--set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
		--set alertmanager.enabled=true \
		--set grafana.enabled=false
	@echo "Waiting for prometheus operator to be ready..."
	kubectl rollout status --watch --timeout=300s deployment/prometheus-stack-kube-prom-operator -n ${MONITORING_NAMESPACE}

	@echo "Install loki"
	helm upgrade --install loki bitnami/grafana-loki \
		--namespace ${MONITORING_NAMESPACE} --create-namespace \
		--set compactor.persistence.size=1Gi \
		--set ingester.persistence.size=1Gi \
		--set querier.persistence.size=1Gi \
		--set ruler.persistence.size=1Gi \
		--set indexGateway.persistence.size=1Gi

	@echo "Waiting for loki querier to be ready..."
	kubectl rollout status --watch --timeout=300s deployment/loki-grafana-loki-query-frontend -n ${MONITORING_NAMESPACE}

	@echo "Install grafana operator"
	helm upgrade --install grafana-operator bitnami/grafana-operator \
		--namespace ${MONITORING_NAMESPACE} --create-namespace \
		--set operator.namespaceScope=false \
		--set operator.watchNamespace="" \
		--set grafana.enabled=false

	@echo "Waiting for grafana operator to be ready..."
	kubectl rollout status --watch --timeout=300s deployment/grafana-operator -n ${MONITORING_NAMESPACE}

	@echo "Setup grafana"
	kubectl apply -f k3d/grafana-v5-api-v1beta1/monitoring-stack-grafana.yaml

	@echo "Waiting for grafana instance to be ready..."
	@sleep 5 # wait for operator to pick up the CRD
	kubectl rollout status --watch --timeout=300s deployment/grafana-deployment -n ${MONITORING_NAMESPACE}

.PHONY: helm-grafana-alpha
.ONESHELL:
helm-grafana-alpha: ## Replace latest grafana operator with version 2.9.3 with v1alpha1 CRDs
	make check-kube-context
	@echo "Uninstall latest grafana operator and CRDs"
	helm uninstall grafana-operator -n ${MONITORING_NAMESPACE}
	make delete-integreatly-crds
	@echo "Cleanup CRDs"
	make delete-grafana-crds

	@echo "Install grafana operator 2.9.3"
	helm upgrade --install grafana-operator bitnami/grafana-operator \
		--namespace ${MONITORING_NAMESPACE} --create-namespace \
		--set operator.scanAllNamespaces=true \
		--set operator.watchNamespace="" \
		--set operator.watchNamespaces="" \
		--set grafana.enabled=false \
		--version 2.9.3

	@echo "Waiting for grafana operator to be ready..."
	kubectl rollout status --watch --timeout=300s deployment/grafana-operator -n ${MONITORING_NAMESPACE}

	@echo "Setup grafana v1alpha1 CRDs	"
	kubectl apply -f k3d/grafana-v4-api-v1alpha1/monitoring-stack-grafana.yaml
	kubectl apply -f k3d/grafana-v4-api-v1alpha1/monitoring-stack-grafana-ds.yaml

	@echo "Waiting for grafana instance to be ready..."
	@sleep 5 # wait for operator to pick up the CRD
	kubectl rollout status --watch --timeout=300s deployment/grafana-deployment -n ${MONITORING_NAMESPACE}

delete-grafana-crds:
	@echo "Deleting CRDs and their instances containing 'integreatly.org'..."
	@kubectl get crds -o name | grep integreatly.org | xargs -I {} sh -c ' \
	  echo "Deleting CRD {} and $$(echo {} | cut -d'/' -f 2-) its instances..."; \
	  kubectl delete $$(echo {} | cut -d'/' -f 2-) --all && kubectl delete {} --timeout=10s --force=true || true; \
	'
	@echo "Deletion complete."

.PHONY: create-test-ns
create-test-ns: ## Create test namespace
	make check-kube-context
	kubectl create namespace ${TEST_NAMESPACE} || true

.PHONY: test-chart
test-chart: ## Run chart-testing 
	make check-kube-context
	make create-test-ns
	ct install --config $(CURDIR)/.github/ct-config.yaml
