<!-- omit in toc -->
# Contributing to conduktor-public-charts

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them. Please make sure to read the relevant section before making your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved. The community looks forward to your contributions. 🎉

> And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
> - Star the project
> - Tweet about it
> - Refer this project in your project's readme
> - Mention the project at local meetups and tell your friends/colleagues

<!-- omit in toc -->
## Table of Contents

- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Your First Code Contribution](#your-first-code-contribution)
- [Improving The Documentation](#improving-the-documentation)
- [Styleguides](#styleguides)
- [Commit Messages](#commit-messages)
- [Join The Project Team](#join-the-project-team)



## I Have a Question

> If you want to ask a question, we assume that you have read the available [Documentation](https://docs.conduktor.io/) and charts READMEs. 

Before you ask a question, it is best to search for existing [Issues](https://github.com/conduktor/conduktor-public-charts/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/conduktor/conduktor-public-charts/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (Kubernetes, Helm, etc), depending on what seems relevant.

We will then take care of the issue as soon as possible.

## I Want To Contribute

### Reporting Bugs

<!-- omit in toc -->
#### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions (Make sure that you have read the [documentation](https://docs.conduktor.io/). If you are looking for support, you might want to check [this section](#i-have-a-question)).
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://github.com/conduktor/conduktor-public-charts/issues?q=label%3Abug).
- Collect information about the bug:
  - Version of the Conduktor chart you are using
  - Version of Conduktor Console or Gateway you are using
  - Log Stack trace (Traceback)
  - Chart values and environment variables
  - Can you reliably reproduce the issue? And can you also reproduce it with older versions?

<!-- omit in toc -->
#### How Do I Submit a Good Bug Report?

> You must never report security related issues, vulnerabilities or bugs including sensitive information to the issue tracker, or elsewhere in public. Instead sensitive bugs must be sent by email to [security@conduktor.io]().

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Issue](https://github.com/conduktor/conduktor-public-charts/issues/new). (Since we can't be sure at this point whether it is a bug or not, we ask you not to talk about a bug yet and not to label the issue.)
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the *reproduction steps* that someone else can follow to recreate the issue on their own. This usually includes your code. For good bug reports you should isolate the problem and create a reduced test case.
- Provide the information you collected in the previous section.

You can also contact us at [support@conduktor.io]() if you need help with the issue.


### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for Conduktor charts, **including completely new features and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.

<!-- omit in toc -->
#### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Read the [documentation](https://docs.conduktor.io/) and charts READMEs carefully and find out if the functionality is already covered, maybe by an individual configuration.
- Perform a [search](https://github.com/conduktor/conduktor-public-charts/issues) to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
- Search for similar suggestions in the [Conduktor Roadmap](https://product.conduktor.help/) and Submit an idea if it is not already there.
- Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset.

<!-- omit in toc -->
#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/conduktor/conduktor-public-charts/issues) or in [Conduktor Roadmap](https://product.conduktor.help/).

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point you can also tell which alternatives do not work for you.
- **Explain why this enhancement would be useful** to most Conduktor charts users. You may also want to point out the other projects that solved it better and which could serve as inspiration.

### Your First Code Contribution

To run the project locally, you will need Helm 3.2.0+ installed and a Kubernetes server with API version 1.19+ available.  
You can also use local K3D clusters and use the `make` commands to start K3D cluster and install the charts.

Here some useful commands to get you started:

Install pre-commit git hooks:
```shell
make install-githooks
```

Run code formatting and linting:
```shell
helm lint charts/gateway
# set mandatory values
helm lint charts/console --set config.organization.name=test,config.admin.email=test@test.io,config.admin.password=test,config.database.password=test,config.database.username=test,config.database.host=test
```

Run local K3D dev cluster:
```shell
# Update helm dependencies
make helm-deps

# Create local K3D cluster for test and local dev (require k3d, helm and kubectl)
make k3d-up

# Install dependencies like a Postgresql, Minio, Monitoring stack, etc.
make install-dev-deps
```

Install chart in local K3D cluster:
```shell
 # Install Conduktor Gateway chart
helm install gateway charts/gateway --namespace conduktor --set kafka.enabled=true 

# Install Conduktor Console chart
helm install console charts/console \
  --namespace conduktor \
  --set config.organization.name=test \
  --set config.admin.email=test@test.io \
  --set config.admin.password=testP4ss! \
  --set config.database.password=conduktor \
  --set config.database.username=postgres \
  --set config.database.host=postgresql.conduktor.svc.cluster.local \
  --set config.database.name=conduktor
```

Update chart readme (require [readme-generator-for-helm](https://github.com/bitnami/readme-generator-for-helm)):
```shell
make generate-readme
```

Run chart tests:
This will start a local K3D cluster and run [chart-testing](https://github.com/helm/chart-testing) (required).
```shell
# Update helm dependencies
make helm-deps
# Create local K3D cluster for test and local dev (require k3d, helm and kubectl)
make k3d-up
# Run Chart-testing tests on chart that contain changes (require chart-testing and helm)
make test-chart
# Delete K3D cluster
make k3d-down
```

Don't forget to run the tests to make sure everything is working as expected before submitting a pull request.

## Styleguides
### Commit Messages
Use explicit commit message that follows the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. This convention makes it easier to understand the changes in a project and to automate the versioning process.


<!-- omit in toc -->
