# Contributing

## Commit Message Format

Each commit message should consist of a **header**, an optional **body**, and a **footer**. The header should be a brief summary of the changes being made and should be no more than 50 characters. The body should provide more detail about the changes being made and should be wrapped at 72 characters. The footer should contain any relevant metadata, such as issue tracking numbers or breaking changes.

```
<type>(<scope>): <subject>

<body>

<footer>
```

- `type` - **Required**. The type of change being made, such as `feat` for a new feature or `fix` for a bug fix.
- `scope` - *Optional*. The scope of the changes being made, such as `server` or `client`.
- `subject` - Required. A brief summary of the changes being made, no more than 50 characters.
- `body` - *Optional*. A more detailed description of the changes being made, ideally wrapped at 72 characters.
- `footer` - *Optional*. Any relevant metadata about the changes being made.

## Commit Message Types

- `feat` - A new feature or enhancement.
- `fix` - A bug fix.
- `docs` - Documentation changes.
- `style` - Changes that do not affect the meaning of the code, such as formatting or white-space changes.
- `refactor` - Code changes that neither fix a bug nor add a feature.
- `test` - Adding missing tests or correcting existing tests.
- `chore` - Changes to the build process or auxiliary tools and libraries such as documentation generation.

## Commit Message Examples



```
feat(server): add support for user authentication

Add support for user authentication using OAuth2.

Closes #1234
```

```
fix(client): resolve issue with navigation menu

Ensure navigation menu is properly aligned and clickable on all screen sizes.

Fixes #5678
```
```
docs: update README.md

Add instructions for running the application locally.
``` 

## Pull Request Guidelines

Please refer to the [Pull Request Template](https://github.com/dessygil/LMS-MSD/blob/main/PULL_REQUEST_TEMPLATE.md).

## Issue Reporting Guidelines

If you encounter an issue with the project, please follow these guidelines when reporting it:

### Steps to Reproduce
Provide a clear and detailed list of steps to reproduce the issue. This should include any necessary context or prerequisites, such as specific settings or conditions that need to be in place.

### Expected Behavior
Describe what you expected to happen when performing the steps to reproduce the issue. This should be a clear and concise description of the desired outcome.

### Actual Behavior
Describe what actually happened when performing the steps to reproduce the issue. This should be a clear and concise description of the current behavior.

### Environment Information
Provide any relevant information about the environment in which the issue occurred. This may include the operating system, browser, or other software used, as well as any specific configurations or settings that may be relevant to the issue.

By following these guidelines, you can help ensure that issues are reported accurately and clearly, making it easier for project contributors to understand and address them.