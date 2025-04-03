# PanelApp

A Python script for creating bed files for the PanelApp gene panels.

## What is PanelApp?

[PanelApp](https://panelapp.genomicsengland.co.uk/) is a website created by Genomics England to provide public access to all gene panels they use. It includes crowdsourcing functionality allowing clinicians nationwide to contribute to the knowledgebase underpinning the website.

## What is the script for?

PanelApp provides downloads of each panel in tsv form. The script takes these tsvs and processes them and then combines them with gene position data from Ensembl Biomart to create bed files that can be used to annotate a vcf file.

## Using the Script

1. Download or clone the repo, not just the tsv.py file, to get the needed folder structure.

2. Place all panels you want to convert in the panels folder.

3. Open a terminal window and navigate to the folder tsv.py is in and run:

```text
python tsv.py
```

4. By default the script will generate hg19/grch37 bed files. To create hg38/grch38 bed files run the script with the optional genome argument, -G or --genome.

```text
python tsv.py -G hg38
```