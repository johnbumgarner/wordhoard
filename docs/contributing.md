<h1><strong>Contributing to WordHoard</strong></h1>
---

<p align="justify">
We're glad that you want to contribute to the <strong>WordHoard</strong> project! This document will help answer common questions you may have during your first contribution or whether it is, such as:
</p>

<ul>
    <li> Reporting a bug </li>
    <li> Discussing the current state of the code </li>
    <li> Submitting a fix </li>
    <li> Proposing new features </li>
    <li> Becoming a maintainer </li>
</ul>


### Submitting Issues

<p align="justify">
Not every contribution comes in the form of code. Submitting, confirming, and triaging issues is an important task for any project. 
</p>

<p align="justify">
At <strong>WordHoard</strong> we use <i>GitHub</i> to track all project issues. Report by <a href="https://github.com/johnbumgarner/wordhoard/issues/new/choose" target="_blank">opening a new issue</a> for the <strong>WordHoard</strong> project. Please write bug or issue reports with as mush detail, background, and sample code as possible. 
</p>

<strong>Great Bug Reports tend to have:</strong>

<ul>
    <li> A quick summary and/or background. </li>
    <li> Steps to reproduce. </li>
    <li> Specific details. </li>
    <li> Sample code. </li>
    <li> What you expected would happen. </li>
    <li> What actually happened. </li>
    <li> Notes (possibly including why you think this might be happening, or stuff you tried that didn't work). </li>
</ul>


### Pull Requests

<p align="justify">
Pull requests are the best way to propose changes to the codebase. <strong>WordHoard</strong> uses <a href="https://guides.github.com/introduction/flow/index.html" target="_blank">Github Flow</a> for this. We actively welcome your pull requests.
</p>

<ol>
    <li> Fork the repository and create your own branch from the <i>master</i>. </li>
    <li> If you've added code that should be tested, add tests. </li>
    <li> If you've changed APIs, update the documentation. </li>
    <li> Ensure the test suite passes. </li>
    <li> Make sure your code lints. </li>
    <li> Issue that pull request! </li>
</ol>


<!-- 
this link is used for email obfuscation 
https://www.willmaster.com/library/generators/resurgence-of-mailto-links.php 
-->

### Reporting a Vulnerability

<p align="justify">
If you have found a security vulnerability in <strong>WordHoard</strong>, or a dependency use, please contact us via <a href="https://wordhoardsupport.slack.com" target="_blank">Slack</a> or through 
<a href="javascript:alert('JavaScript')" onclick="this.href=atob('bWFpbHRvOndvcmRob2FyZHByb2plY3QlNDBnbWFpbC5jb20/c3ViamVjdD1Xb3JkSG9hcmQlMjBwcm9qZWN0JTIwc2VjdXJpdHklMjBpc3N1ZQ=='); return true">email</a>.
</p>

<p align="justify">
Please join the <strong>#wordhoard-project</strong> channel and say that you believe you have found a security issue. One of the <strong>WordHoard</strong> Support members will send you a direct message to understand the problem. Once the problem is understood a newly created private channel will be created by the Member and you will be invited to explain the problem further.
</p>

<p align="justify">
Please provide a <a href="http://sscce.org" target="_blank">concise reproducible test case</a> and describe what results you are seeing and what results you expect.
</p>


### Developer Certification of Origin (DCO)

<p align="justify">
Licensing is very important to open source projects. It helps ensure the software continues to be available under the terms that the author desired.
</p>

<p align="justify">
<strong>WordHoard</strong> uses the <a href="http://choosealicense.com/licenses/mit" target="_blank">MIT License</a> to strike a balance between open contribution and allowing you to use the <strong>WordHoard</strong> package in other projects.
</p>

<p align="justify">
The license tells you what rights you have that are provided by the copyright holder. It is important that the contributor fully understands what rights they are licensing and agrees to them. Sometimes the copyright holder isn't the contributor, such as when the contributor is doing work on behalf of a company.
</p>

<p align="justify">
To make a good faith effort to ensure these criteria are met, <strong>WordHoard</strong> requires the Developer Certificate of Origin (DCO) process to be followed.
</p>

<p align="justify">
The DCO is an attestation attached to every contribution made by every developer. In the commit message of the contribution, the developer simply adds a Signed-off-by statement and thereby agrees to the DCO.
</p>

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

### DCO Sign-Off Methods

The DCO requires a sign-off message in the following format appear on each commit in the pull request:

```
Signed-off-by: Super Coder <supercoder@somedomain.com>
```
<p align="justify">
The DCO text can either be manually added to your commit body, or you can add either `-s` or `--signoff` to your usual git commit commands. If you are using the <i>GitHub</i> UI to make a change you can add the sign-off message directly to the commit message when creating the pull request. If you forget to add the sign-off you can also amend a previous commit with the sign-off by running `git commit --amend -s`. If you've pushed your changes to <i>GitHub</i> already you'll need to force push your branch after this with `git push -f`.
</p>

### Obvious Fix Policy

<p align="justify">
Small contributions, such as fixing spelling errors, where the content is small enough to not be considered intellectual property, can be submitted without signing the contribution for the DCO.
</p>

<p align="justify">
As a rule of thumb, changes are obvious fixes if they do not introduce any new functionality or creative thinking. Assuming the change does not affect functionality, some common obvious fix examples include the following:
</p>

<ul>
    <li> Spelling/grammar fixes. </li>
    <li> Typo correction, white space and formatting changes. </li>
    <li> Comment clean up. </li>
    <li> Bug fixes that change default return values or error codes stored in constants. </li>
    <li> Adding logging messages or debugging output. </li>
    <li> Changes to 'metadata' files like .gitignore, build scripts, etc. </li>
    <li> Moving source files from one directory or package to another. </li>
</ul>

<p>
Whenever you invoke the "obvious fix" rule, please say so in your commit message: 
<br>

------------------------------------------------------------------------ <br>
commit 370adb3f82d55d912b0cf9c1d1e99b132a8ed3b5<br>
Author: Super Coder <supercoder@somedomain.com> <br>
Date:   Fri Aug 13 14:00:40 2021 -0500 <br>
<br>
Fix typo in the README. <br>
<br>
Obvious fix.<br>
------------------------------------------------------------------------ <br>
</p>
