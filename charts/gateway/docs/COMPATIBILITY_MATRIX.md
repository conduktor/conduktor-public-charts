# Conduktor Gateway Compatibility Matrix
This compatibility matrix is a resource to help you find which versions of Conduktor Gateway work on which version of our Conduktor Gateway Helm Chart.

> General recommendation is to use the version of Gateway that comes preconfigured with the helm chart. If needed you can adjust the version in your values property according to the supported console version.

> Breaking changes column will only list breaking change in the helmchart! We strongly recommend reading the full [changelog](https://docs.conduktor.io/changelog/) of Conduktor in case there are breaking within the components.

## Helm Chart Compatibility

Breaking Changes:

🟡 - Breaks additional services (e.g. Grafana dashboard changes)

🔴 - Breaks overall deployment of product (e.g. renaming variables in .values, major product releases)

| Chart version | Supported Gateway version | Breaking changes |
|---------------|---------------------------|------------------|
| [conduktor-gateway-3.3.1](https://github.com/conduktor/conduktor-public-charts/releases/tag/conduktor-gateway-3.3.1) | 3.3.1, 3.3.0, 3.2.2, 3.2.1, 3.2.0, 3.1.1, 3.1.0 | |
| [conduktor-gateway-3.3.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/conduktor-gateway-3.3.0) | 3.3.0, 3.2.2, 3.2.1, 3.2.0, 3.1.1, 3.1.0 | |
| [conduktor-gateway-3.2.2](https://github.com/conduktor/conduktor-public-charts/releases/tag/conduktor-gateway-3.2.2) | 3.2.2, 3.2.1, 3.2.0, 3.1.1, 3.1.0 | 🟡 Updated Grafana template [see here](https://github.com/conduktor/conduktor-public-charts/pull/98) |
| [conduktor-gateway-3.2.1](https://github.com/conduktor/conduktor-public-charts/releases/tag/conduktor-gateway-3.2.1) | 3.2.1, 3.2.0, 3.1.1, 3.1.0 | |
| [conduktor-gateway-3.2.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/conduktor-gateway-3.2.0) | 3.2.1, 3.2.0, 3.1.1, 3.1.0 | |
| [conduktor-gateway-3.1.1](https://github.com/conduktor/conduktor-public-charts/releases/tag/conduktor-gateway-3.1.1) | 3.1.1, 3.1.0 | |
| [conduktor-gateway-3.1.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/conduktor-gateway-3.1.0) | 3.1.1, 3.1.0 | 🟡 Updated Grafana template [see here](https://github.com/conduktor/conduktor-public-charts/pull/81)|
| [conduktor-gateway-3.0.1](https://github.com/conduktor/conduktor-public-charts/releases/tag/conduktor-gateway-3.0.1) | 3.0.1, 3.0.0 | |
| [conduktor-gateway-3.0.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/conduktor-gateway-3.0.0) | 3.0.0 | 🔴 Major product update [see here](https://github.com/conduktor/conduktor-public-charts/pull/56) |