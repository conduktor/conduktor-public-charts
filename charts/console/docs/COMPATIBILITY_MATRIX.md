# Conduktor Console Compatibility Matrix
This compatibility matrix is a resource to help you find which versions of Conduktor Console work on which version of our Conduktor Console Helm Chart.

> General recommendation is to use the version of Console that comes preconfigured with the helm chart. If needed you can adjust the version in your values property according to the supported console version.

> Breaking changes column will only list breaking change in the helmchart! We strongly recommend reading the full [changelog](https://docs.conduktor.io/changelog/) of Conduktor in case there are breaking within the components.

## Helm Chart Compatibility

Breaking Changes:

🟡 - Breaks additional services (e.g. Grafana dashboard changes)

🔴 - Breaks overall deployment of product

| Chart version | Supported Console version | Breaking changes |
|---------------|---------------------------|------------------|
| [console-1.13.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.13.0) | 1.28.0, 1.27.1, 1.27.0, 1.26.0, 1.25.1, 1.25.0, 1.24.1, 1.24.0 | |
| [console-1.12.1](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.12.1) | 1.27.1, 1.27.0, 1.26.0, 1.25.1, 1.25.0, 1.24.1, 1.24.0 | |
| [console-1.12.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.12.0) | 1.27.0, 1.26.0, 1.25.1, 1.25.0, 1.24.1, 1.24.0 | |
| [console-1.11.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.11.0) | 1.26.0, 1.25.1, 1.25.0, 1.24.1, 1.24.0 |
| [console-1.10.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.10.0) | 1.25.1, 1.25.0, 1.24.1, 1.24.0 | |
| [console-1.9.1](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.9.1) | 1.24.1, 1.24.0 | |
| [console-1.9.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.9.0) | 1.24.0 | 🔴 Changed liveness and readiness probe path [see here](https://github.com/conduktor/conduktor-public-charts/pull/80) |
| [console-1.8.1](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.8.1) | 1.23.0, 1.22.1, 1.22.0 | |
| [console-1.8.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.8.0) | 1.23.0, 1.22.1, 1.22.0 | |
| [console-1.7.2](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.7.2) | 1.22.1, 1.22.0 | 🔴 Service Monitor endpoint changes, Grafana template changes [see here](https://github.com/conduktor/conduktor-public-charts/pull/65) |
| [console-1.6.2](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.6.2) | 1.21.3, 1.21.2, 1.21.1, 1.21.0 | |
| [console-1.6.1](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.6.1) | 1.21.1, 1.21.0 | |
| [console-1.6.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.6.0) | 1.21.0 | 🔴 Paths and folder changed [see here](https://github.com/conduktor/conduktor-public-charts/pull/54) |
| [console-1.5.5](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.5.5) | 1.20.0, 1.19.2, 1.19.1, 1.19.0, 1.18.4, 1.18.2, 1.18.1, 1.18.0, 1.17.3 | |
| [console-1.5.4](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.5.4) | 1.20.0, 1.19.2, 1.19.1, 1.19.0, 1.18.4, 1.18.2, 1.18.1, 1.18.0, 1.17.3 | 🟡 Updated Grafana template [see here](https://github.com/conduktor/conduktor-public-charts/pull/49) |
| [console-1.5.3](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.5.3) | 1.20.0, 1.19.2, 1.19.1, 1.19.0, 1.18.4, 1.18.2, 1.18.1, 1.18.0, 1.17.3 | 🟡 Updated Grafana template [see here](https://github.com/conduktor/conduktor-public-charts/pull/47) |
| [console-1.5.2](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.5.2) | 1.20.0, 1.19.2, 1.19.1, 1.19.0, 1.18.4, 1.18.2, 1.18.1, 1.18.0, 1.17.3 | 🟡 Updated Grafana template [see here](https://github.com/conduktor/conduktor-public-charts/pull/44) |
| [console-1.5.1](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.5.1) | 1.20.0, 1.19.2, 1.19.1, 1.19.0, 1.18.4, 1.18.2, 1.18.1, 1.18.0, 1.17.3 | |
| [console-1.5.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.5.0) | 1.20.0, 1.19.2, 1.19.1, 1.19.0, 1.18.4, 1.18.2, 1.18.1, 1.18.0, 1.17.3 | |
| [console-1.4.2](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.4.2) | 1.19.2, 1.19.1, 1.19.0, 1.18.4, 1.18.2, 1.18.1, 1.18.0, 1.17.3 | |
| [console-1.4.1](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.4.1) | 1.19.1, 1.19.0, 1.18.4, 1.18.2, 1.18.1, 1.18.0, 1.17.3 | |
| [console-1.4.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.4.0) | 1.19.0, 1.18.4, 1.18.2, 1.18.1, 1.18.0, 1.17.3 | |
| [console-1.3.9](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.3.9) | 1.18.4, 1.18.2, 1.18.1, 1.18.0, 1.17.3 | |
| [console-1.3.8](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.3.8) | 1.18.4, 1.18.2, 1.18.1, 1.18.0, 1.17.3 | |
| [console-1.3.7](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.3.7) | 1.18.3, 1.18.2, 1.18.1, 1.18.0, 1.17.3 | |
| [console-1.3.6](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.3.6) | 1.18.2, 1.18.1, 1.18.0, 1.17.3 | |
| [console-1.3.5](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.3.5) | 1.18.1, 1.18.0, 1.17.3 | |
| [console-1.3.4](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.3.4) | 1.18.1, 1.18.0, 1.17.3 | |
| [console-1.3.3](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.3.3) | 1.18.1, 1.18.0, 1.17.3 | |
| [console-1.3.2](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.3.2) | 1.18.0, 1.17.3 | |
| [console-1.3.1](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.3.1) | 1.18.0, 1.17.3 | |
| [console-1.3.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.3.0) | 1.18.0, 1.17.3 | |
| [console-1.2.4](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.2.4) | 1.17.3 | |
| [console-1.2.3](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.2.3) | 1.17.3 | |
| [console-1.2.2](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.2.2) | 1.17.3 | |
| [console-1.2.1](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.2.1) | 1.17.3 | |
| [console-1.2.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.2.0) | 1.17.3 | |
| [console-1.1.4](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.1.4) | 1.17.3 | 🔴 Fixed issue with license checksum [see here](https://github.com/conduktor/conduktor-public-charts/pull/14) |
| [console-1.1.3](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.1.3) | 1.17.3, 1.17.2 | |
| [console-1.1.2](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.1.2) | 1.17.3, 1.17.2 | |
| [console-1.1.1](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.1.1) | 1.17.3, 1.17.2 | |
| [console-1.1.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.1.0) | 1.17.3, 1.17.2 | |
| [console-1.0.3](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.0.3) | 1.17.3, 1.17.2 | |
| [console-1.0.2](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.0.2) | 1.17.3, 1.17.2 | |
| [console-1.0.1](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.0.1) | 1.17.3, 1.17.2 | |
| [console-1.0.0](https://github.com/conduktor/conduktor-public-charts/releases/tag/console-1.0.0) | 1.17.2 | |