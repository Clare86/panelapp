# PanelApp

A Python script for creating bed files for PanelApp gene panels.

## What is PanelApp?

PanelApp is a website created by Genomics England to provide public access to all gene panels they use. It includes crowdsourcing functionality allowing clinicians nationwide to contribute to the knowledgebase underpinning the website.

## What is the script for?

PanelApp provides downloads of each panel in tsv form. The script takes these tsvs and processes them and then combines them with gene position data from Ensembl Biomart to create bed files that can be used to annotate a vcf file.

## Using the Script

Download or clone the repo

To run open a terminal window and navigate to the folder tsv.py is in and run:

```text
$ python tsv.py
```