import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser(description='Description of your app here.')
parser.add_argument('-I', '--input', help='Choose a single panel to create bed file for.')
parser.add_argument('-G', '--genome', default="hg19",  help='Choose a reference genome.')

folder = os.path.dirname(__file__)

def load_genes(genome):
    # LOAD DATA
    if genome == "hg19":
        genes = pd.read_csv(folder+'/genes/mart_export_hg19_hgnc.tsv', sep='\t', dtype={"Chromosome/scaffold name":str})
    elif genome == "hg38":
        genes = pd.read_csv(folder+'/genes/mart_export_hg38_hgnc.tsv', sep='\t', dtype={"Chromosome/scaffold name":str})
        # SPLIT HGNC COLUMN TO GET JUST NUMBER
        genes['HGNC ID'] = genes['HGNC ID'].str.split(':').str[1]

    # CONVERT GENES HGNC COLUMN TO INT
    genes['HGNC ID'] = genes['HGNC ID'].astype('Int64')

    # REMOVE ALTERNATE CONTIGS FROM GENES LIST
    chroms = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","X","Y","MT"]
    genes = genes[genes["Chromosome/scaffold name"].isin(chroms)]

    # CREATE CHROM ORDER COLUMN
    chroms = {"X":23,"Y":24,"MT":25}
    genes["chrom_order"] = genes["Chromosome/scaffold name"]
    genes = genes.replace({"chrom_order":chroms})
    genes['chrom_order'] = genes['chrom_order'].apply(pd.to_numeric).astype('Int64')

    return genes

def load_panel(panel_tsv):
    # LOAD DATA
    panel = pd.read_csv(folder+'/panels/'+panel_tsv, sep='\t')

    # SPLIT panel_tsv APP HGNC COLUMN
    panel['HGNC ID'] = panel['HGNC'].str.split(':').str[1]

    # CONVERT GENES HGNC COLUMN TO INT
    panel['HGNC ID'] = panel['HGNC ID'].astype('Int64')

    # FILTER PANEL TO JUST GENES
    panel = panel[panel["Entity type"] =="gene"]

    # EDIT COLUMNS
    # REPLACE GEL_STATUS (CONFIDENCE LEVELS) NUMBERS WITH COLOURS
    status = {3:"Green",2:"Amber",1:"Red",0:"Grey"}
    panel = panel.replace({"GEL_Status":status})
    
    # REPLACE WHITESPACE
    panel[["Phenotypes","Model_Of_Inheritance"]] = panel[["Phenotypes","Model_Of_Inheritance"]].replace(" ", "_", regex=True)

    # Agregate confidence, phenotype and inheritance columns
    panel = panel.drop_duplicates().fillna("")
    panel = panel.groupby(["Gene Symbol","HGNC ID"]).agg(
        GEL_Status=("GEL_Status", lambda x: ','.join(x.unique())),
        Model_Of_Inheritance=("Model_Of_Inheritance", lambda x: ','.join(x.unique())),
        Phenotypes=("Phenotypes", lambda x: ','.join(x.unique()))
    )

    return panel


def create_bed(bedname,panel,genes,genome):
    # JOIN DATAFRAMES ON HGNC ID
    bed = pd.merge(panel, genes, on='HGNC ID', how='inner')

    # SORT BY CHROM AND START AND FLATTEN HEADERS
    bed = bed.sort_values(["chrom_order","Gene start (bp)"], ascending=[True, True]).reset_index()

    # SELECT COLUMNS
    bed = bed[["Chromosome/scaffold name","Gene start (bp)","Gene end (bp)","HGNC symbol","GEL_Status","Model_Of_Inheritance","Phenotypes"]]

    # print(bed.head(10))

    # MAKE OUTPUT DIRECTORY IF IT DOESN'T ALREADY EXIST
    if not os.path.exists(folder+"/output/"+genome):
        os.makedirs(folder+"/output/"+genome)

    # SAVE OUTPUT TO BED FILE
    bed.to_csv(folder+"/output/"+genome+"/"+bedname, sep='\t', index=False, header=None)

def create_output(filename,genes):
    if filename.endswith(".tsv"): 
            print(filename)
            panel = load_panel(filename)
            bedname = filename.replace('tsv', 'bed')
            create_bed(bedname,panel,genes,genome)
    else:
        print("Not a tsv file.")


#hg19_genes = load_genes("hg19")
#hg38_genes = load_genes("hg38")

# SINGLE PANEL
# panel_tsv = "Mendeliome.tsv"
# panel = load_panel(panel_tsv)
# create_bed(panel_tsv,panel,hg19_genes,"hg19")


if __name__ == "__main__":
    args = parser.parse_args()

    # GET GENE POSITIONS FOR SPECFIED REFERENCE GENOME
    genome = args.genome
    if genome == "hg38":
        genes = load_genes("hg38")
    else:
        genome == "hg19"
        genes = load_genes("hg19")

    # IF A SINGLE PANEL WAS SPECIFIED ONLY CREATE OUTPUT FOR THAT PANEL
    inputpanel = args.input
    if inputpanel:
        create_output(inputpanel,genes)
    # ELSE LOOP THROUGH ALL PANELS IN PANELS FOLDER
    else:
        for file in os.listdir(folder+"/panels"):
            filename = os.fsdecode(file)
            create_output(filename,genes)