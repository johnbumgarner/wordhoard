<h1 style="color:IndianRed;">Contributing to Wordhoard</h1>

___
We're glad that you want to contribute to the Wordhoard project! This document will help answer common questions you may have during your first contribution or whether it is, such as:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

<h2 style="color:IndianRed;">Submitting Issues</h2>

Not every contribution comes in the form of code. Submitting, confirming, and triaging issues is an important task for any project. 

At Wordhoard we use GitHub to track all project issues. Report by [opening a new issue](https://github.com/johnbumgarner/wordhoard/issues/new/choose) for the Wordhoard project.

Write bug or issue reports with detail, background, and sample code:

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can. 
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

<h2 style="color:IndianRed;">Pull Requests</h2>

Pull requests are the best way to propose changes to the codebase (we use [Github Flow](https://guides.github.com/introduction/flow/index.html)). We actively welcome your pull requests:

1. Fork the repo and create your branch from `master`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

<h2 style="color:IndianRed;">Reporting a Vulnerability</h2>

If you have found a security vulnerability in *Wordhoard*, or a dependency use, please contact us on [Slack](https://wordhoardsupport.slack.com) or via email me at [Wordhoard project](mailto:wordhoardproject@gmail.com?subject=[GitHub]%20wordhoard%20project%20security%20issue).

Please join the `#wordhoard-project` channel and say that you believe you have found a security issue. 
One of the Wordhoard Support members will send you a direct message to understand the problem. Once the problem is understood a newly created private channel
will be created by the Member and you will be invited to explain the problem further.

Please provide a [concise reproducible test case](http://sscce.org/) and describe what results you are seeing and what results you expect.


<h2 style="color:IndianRed;">Developer Certification of Origin (DCO)</h2>

Licensing is very important to open source projects. It helps ensure the software continues to be available under the terms that the author desired.

Wordhoard uses the [MIT License](http://choosealicense.com/licenses/mit/) to strike a balance between open contribution and allowing you to use the Wordhoard package in other projects.

The license tells you what rights you have that are provided by the copyright holder. It is important that the contributor fully understands what rights they are licensing and agrees to them. Sometimes the copyright holder isn't the contributor, such as when the contributor is doing work on behalf of a company.

To make a good faith effort to ensure these criteria are met, Wordhoard requires the Developer Certificate of Origin (DCO) process to be followed.

The DCO is an attestation attached to every contribution made by every developer. In the commit message of the contribution, the developer simply adds a Signed-off-by statement and thereby agrees to the DCO.

```
Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the
    best of my knowledge, is covered under an appropriate open
    source license and I have the right under that license to
    submit that work with modifications, whether created in whole
    or in part by me, under the same open source license (unless
    I am permitted to submit under a different license), as
    Indicated in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including
    all personal information I submit with it, including my
    sign-off) is maintained indefinitely and may be redistributed
    consistent with this project or the open source license(s)
    involved.
```

<h1 style="color:IndianRed;">DCO Sign-Off Methods</h1>

___

The DCO requires a sign-off message in the following format appear on each commit in the pull request:

```
Signed-off-by: Super Coder <supercoder@somedomain.com>
```

The DCO text can either be manually added to your commit body, or you can add either -s or --signoff to your usual git commit commands. If you are using the GitHub UI to make a change you can add the sign-off message directly to the commit message when creating the pull request. If you forget to add the sign-off you can also amend a previous commit with the sign-off by running git commit --amend -s. If you've pushed your changes to GitHub already you'll need to force push your branch after this with git push -f.

<h2 style="color:IndianRed;">Wordhoard Obvious Fix Policy</h2>

Small contributions, such as fixing spelling errors, where the content is small enough to not be considered intellectual property, can be submitted without signing the contribution for the DCO.

As a rule of thumb, changes are obvious fixes if they do not introduce any new functionality or creative thinking. Assuming the change does not affect functionality, some common obvious fix examples include the following:

Spelling / grammar fixes
Typo correction, white space and formatting changes
Comment clean up
Bug fixes that change default return values or error codes stored in constants
Adding logging messages or debugging output
Changes to 'metadata' files like .gitignore, build scripts, etc.
Moving source files from one directory or package to another
Whenever you invoke the "obvious fix" rule, please say so in your commit message:

------------------------------------------------------------------------
commit 370adb3f82d55d912b0cf9c1d1e99b132a8ed3b5
Author: Super Coder <supercoder@somedomain.com>
Date:   Fri Aug 13 14:00:40 2021 -0500

  Fix typo in the README.

  Obvious fix.

------------------------------------------------------------------------

