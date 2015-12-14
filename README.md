# Static Website Generator

## Goal
Generate **static webpages** (HTML files) suitable for uploading to a web
hosting via FTP from **Markdown documents** formatted by **Jinja2 templates**
and attach **static resources** (CSS, PNG, JPG files) used by the webpages.

Generate **paginated lists sorted by date** pointing to webpages marked by a
**tag**.

Generate **Google-compatible sitemap** pointing to recent and selected
documents and **RSS/Atom feed** pointing to recent documents.

Use URLs pointing either to local filesystem (`file://`) for **debugging
before publishing** or to a webserver (`http://`) for the **publishing**
to a real webserver.

## Use Case
1. For each webpage of the website:<br/>
   The user provides a **document** containing textual contents of the webpage
   and metadata selecting the _template_ and _features_ of the webpage. (\*)
2. For each template referenced by the documents:<br/>
   The user provides a **template** describing the appearance of the webpage.
3. For each static resource referenced by the documents and templates:<br/>
   The user provides the **resource** file.
4. The user asks the generator to build the website from provided documents,
   templates and resources using **local filesystem** for the URLs.
6. For each document:<br/>
   The generator creates a webpage
6. For each tag referenced by the documents:<br/>
   The generator creates **paginated list** sorted by date pointing to webpages
   marked by given tag.
7. The user **displays and checks** the generated webpage in a browser using
   files on the local filesystem.
8. The user assk the generator to re-build the final version of the website
   using a **remote webserver** for the URLs.
9. The user **uploads** the rebuilt website to the webhosting **via FTP**.

(\*) The **sitemap** and **RSS feed** are regular documents with a corresponding
template (`sitemap.xml` and `atom.xml`).

## Usage
`python3 generator.py`

## Installation
Prerequisites: **Python 3** (tested using Python 3.4.3 on Ubuntu 15.10)<br/>
`git checkout https://github.com/TODO`<br/>
`pip install markdown jinja2`

## File Formats
Each document consists of two parts, delimited by a blank line:
- **Metadata**: key:value dictionary with webpage metadata in **YAML** format
- **Contents**: text of the webpage in **Markdown** format

### Document Metadata
The metadata of each document should contain at least the following keys:
- **template**: mandatory for all documents, used for HTML/XML rendering
- **date**: mandatory for documents with a tag, used for paginated list sorting
- **tags**: mandatory for documents to be added to a paginated list
- **title**: recommended for SEO via HTML &lt;title&gt;
- **description**: recommended for SEO via HTML
  &lt;meta name="description"/&gt;
- **keywords**: recommended for SEO via HTML &lt;meta name="keywords"/&gt;

The `template` value has to contain the whole filename, its suffix is used as a
suffix for the exported HTML/XML file to the filesystem.

Mandatory keys are used by the generator itself, recommended keys should be used
by the templates (example templates do so), using any other keys is possible and
purely depends on their usage in the templates. Missing keys are replaced by
_None_. Keys and their values are case-sensitive, leading and trailing
whitespaces are stripped out.

## Filesystem Structure
- **Website**
  - **Markdown documents**: `documents/\*`
  - **Jinja2 templates**: `templates/\*.{html | xml}`
  - **Static resources**: `resources/\*.{jpg | png | css | ...}`
  - **Generated website**: `generated/\*.{html | xml}`

### URLs in the Markdown
The references to images from Markdown use just the filename (**with** the file
extension and without quotes) and the generator automatically points them to the
resource folder (regardless if at the local filesystem or on a web server).
<br/>Example: `![picture.png](A picture)` is translated to
`file:///home/user/generator/generated/static/picture.png` or to
`http://website.domain/static/picture.png`

Likewise, the links to another documents from the Markdown use just the document
name (without the file extension and without quotes) and the generator
automatically points them to the generated webpage for given document.
<br/>Example: `[about-us](About us)` is translated to
`file:///home/user/generator/generated/about-us.html` or to
`http://website.domain/about-us.html`

If a resource document or a document is located in a subfolder, the reference
from the Markdown should include the subfolder.
<br/>Example: `[blog/interesting-blogpost](Interesting Blogpost)` is translated
to `file:///home/user/generator/generated/blog/interesting-blogpost.html` or to
`http://website.domain/blog/interesting-blogpost.html`

### Template Features
The templates can leverage any features of Jinja2 templating engine, however the
most useful ones are:
- **Inheritance**: a template can reuse parts of another template via
  `{% include %}`
- **Inclusion**: a template can reuse an external file via `{% include %}`
- **Markdown**: any part of the template/external file can use Markdown format
  surrounded by `{% filter markdown %}` (do not indentat the Markdown contents
  otherwise it will be interpreted as preformatted)
- **Conditions**: rendering of the document into HTML can depend on a value of
  given document's metadata (e. g. first page of a list) or a website-globals
- **Loops**: document's rendered HTML can contain repeating parts based on given
  document's metadata or website-globals (e .g. few newest blog posts)

## Markdown in Templates
Jinja2 templates do not support rendering of Markdown into HTML out of the box.
Generator implements a **custom Jinja2 filter** named `markdown` which delegates
the rendering of Markdown to Python Markdown module.

If the template wraps the Markdown text by `{% filter markdown %}` and
`{% endfilter %}`, the rendered HTML is then added to the rendered webpage.
<br/>Example:
```
<html>
  <head/>
  <body>
    {% filter markdown %}
      { document.markdown_contents }
    {% endfilter %}
  </body>
</html>
```

## Referencing the Documents from Templates
The generator provides a reference to the **rendered document** as `document`
(allowing access to the document's metadata) and a reference to a dictionary of
**all documents of the website** as `documents` (allowing access to other
documents' metadata, useful for example for displaying last few blog posts in
the sidebar).

References to other documents must contain the whole filename (and canonical
path relative to the site root if the referenced document is located in a
subfolder), use **document filenames without an extension**.

## Paginated Timelines
The generator automatically generated webpages with a paginated list sorted by
date with references to all documents having a tag. **Attach a tag to all blog
posts** to have the timeline generated automatically.

The tag name serves as a name of **virtual folder** located under the site root
(beware of conflicts with folder names of the documents).

The tag name with `.html` suffix serves as a name of the **template** used for
rendering of all pages of the paginated timeline.

**Categories** can be also provided via the tags.

## Internals

### class ResourceExtension
- Markdown Extension
- Replaces Markdown image links by `{{ resource() }}` placeholder

### class UrlForExtension
- Markdown Extension
- Replaces Markdown links by `{{ url_for() }}` placeholder

### class Document
- One Markdown document
- Loads the document from filesystem, parses YAML metadata and Markdown contents

### class Templates
- All Jinja2 templates used by the website (including the paginated timelines)
- Loads the templates from filesystem
- Adds Markdown support to the templates
- Adds absolute URL support to the templates
- Adds current date and time support to the templates
- Adds custom template-globals to the templates

Uses: `class ResourceExtension`, `class UrlForExtension`, `module Markdown`,
`module Jinja2`

### class DocumentGenerator
- All webpages for the Markdown documents
- Loads all documents from the filesystem
- Renders all documents into HTML/XML
- Exports all rendered HTML/XMLs to the filesystem
- Finds the template for given document
- Injects reference to rendered document and to all documents into the template

Uses: `class Templates`, `class Document` list

### class TimelinePages
- All pages of the paginated timeline
- Builds a timeline from all documents having given tag (by sorting them by date)
- Splits the timeline into pages holding piecemeals of the documents
- Finds neighbor pages to each timeline page

Uses: `class Document` list

### class TimelinePagesGenerator
- All webpages for pages of one timeline
- Renders all pages of the timeline into HTML (XML is not supported)
- Exports all rendered HTML documents to the filesystem

Uses: `class TimelinePages`

### class Website
- Finds all tags used by the website
- Builds the whole website
uses: `class DocumentGenerator`, `class TimelinePagesGenerator` list, website
root (commandline argument)
