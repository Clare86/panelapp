# PanelApp

A Python script for creating bed files for the PanelApp gene panels.

## What is PanelApp?

[PanelApp](https://panelapp.genomicsengland.co.uk/) is a website created by Genomics England to provide public access to all gene panels they use. It includes crowdsourcing functionality allowing clinicians nationwide to contribute to the knowledgebase underpinning the website.

## What is the script for?

PanelApp provides downloads of each panel in tsv form. The script takes these tsvs and processes them and then combines them with gene position data from Ensembl Biomart to create bed files that can be used to annotate a vcf file.

By deafult the script will run through all tsv files in the panels folder and create hg19 bed files for them. See the below section on optional parameters for additional functionality.

## Using the Script

1. Download or clone the repo, not just the tsv.py file, to get the needed folder structure. The panels and genes folders along with the contents of the genes folder are necessary.

2. Download the panels you want to convert from [PanelApp](https://panelapp.genomicsengland.co.uk/) and place in the panels folder.

3. Open a terminal window and navigate to the tsv folder and run:

```text
python tsv.py
```

4. When complete the bed files can be found in the output folder.

## Optional Paramters

Two optional parameters are available for additional functionality.

| Short Form | Long Form | Description |
| ---------- | -------- | ----------- |
| -G | --genome | Specify the reference genome; hg19 or hg38. Default is hg19. |
| -I | --input | Specify a single panel instead of running through all panels. |

### Example

To create a hg38 bed file for the Congenital Myopathy panel.

```text
python tsv.py -G hg38 -I "Congenital myopathy.tsv"
```