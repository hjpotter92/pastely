pastely
=======

The project is a monorepo for the pet "pastely" project.

## Introduction

It is yet another code/snippet sharing project, with a minor link
shortening feature built-in.

The project relies heavily on AWS services for the initial version.

## Features

The planned/implemented features (in no particular order are):

  - Share code snippet
  - Set expiry for snippets
  - Protect snippets with a password
  - Parse the pasted content for single URL, in which case it'd be
    interpreted as a URL shortener
  - Store project configuration across AWS S3 and AWS DyanamoDB
  - Allow for code highlighting when using the browser
  - API to fetch raw file (or simple CDN/AWS cloudfront link?)
  - Add title/description to snippets (à la gist.github)
  - Use AWS lambda to alleviate need for machines
  - Deploy front-end application using github pages or vercel

## Licence

Project is MIT licence.
