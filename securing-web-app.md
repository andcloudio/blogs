# Securing Web App

## OWASP Zed Attack Proxy (ZAP)

- open source tool designed to scan web apps for vulnerabilities.

- Integrate ZAP Docker container to run a baseline scan on application container in CI pipeline.

## cross-site scripting attack (XSS)

- XSS attacks are caused by injecting fraudulent code into a website that’s later reflected to other site visitors as if it was normal content. 

- It can be prevented with input validation and output encoding, enabling Content Security Policy (CSP) built into web browsers.

## Cross-Site Request Forgery 

- Cross-site request forgery attacks abuse links between websites and should be prevented via CSRF tokens.

## Clickjacking and Iframes protection

- Clickjacking is an abuse of IFrames that applications can stop via CSP and X-Frame-Options headers.

## HTTP Authentication

- Web applications should authenticate users via identity providers whenever possible to avoid storing passwords locally.

## Sessions AND Cookie Security

- An application must create a session once the user is authenticated, and check the validity of the session when new requests are received.

- Stateful sessions store a session ID in a database and verify that the user sent the ID with every request.

- Stateless sessions don’t store data on the server side, but simply verify that the user possesses a trusted and recent session cookie.

## Managing dependencies

- Programming languages provide mechanisms to keep applications up to date, that can be integrated into CI testing.

- For node.js, nsp uses various databases of known vulnerabilities to look for packages that may be out of date and exposed to security issues. 

- For python pip command-line tool provides an option to test for outdated dependencies

- online services like https://requires.io or https://pyup.io/ provide ways to assert the vulnerability of Python applications. 