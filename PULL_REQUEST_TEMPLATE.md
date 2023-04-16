## Description
Describe the context and requirements for this change.

```
Try to answer the following questions:
Who – Who is contributing?
What – What is the change?
When – When is the change needed by?
Where – What feature(s) are dependent on the change?
Why – Why is this change needed?
```
## Screenshots
If there are any visual changes, please include relevant screenshots. Otherwise, remove this section.

## Relevant Issues
Link any relevant GitHub issues and/or pull requests.

## Impact
What impact will this change have on the project?

- [ ] `Low` – A non-breaking change that will not affect the overall functionality of the application.
    - Adding a new comment to the codebase to clarify a particular function or method.
    - Adding new tests or modifying existing tests to improve code coverage.
    - Fixing a bug that does not affect the overall functionality of the application.
    - Adding a new debug statement or logging message to the codebase.
    - Refactoring code to improve readability or performance without changing its functionality.
- [ ] `Medium` – A breaking change this is limited to a few specific components and/or consumers.
    - Changing the name or data type of a specific field in an API that is used by a few specific consumers.
    - Updating the interface of a specific module in a codebase that is only used by a few other modules.
    - Adding a new required configuration parameter to a specific module or function in a codebase that is used by a few other modules.
- [ ] `High` –  A breaking change that is difficult to quantify and/or extends to several components and/or consumers.
    - Removing a critical feature from a product that is used by a large portion of its users.
    - Refactoring a core library or component that is used by multiple other libraries or components in a codebase.
    - Changing the database schema or architecture of an application that affects many different parts of the system.

## Checklist:

- [ ] I have read the [Contribution Guidelines](https://github.com/dessygil/LMS-MSD/blob/main/CONTRIBUTING.md)
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published in downstream modules