"""
Code heavily inspired by @Hrvoje from https://stackoverflow.com/questions/57053378/query-pubmed-with-python-how-to-get-all-article-details-from-query-to-pandas-d
"""

# Import Packkages
from pymed import PubMed
import pandas as pd

# Index of gain of function and loss of function genes
# Taken from: https://www.cancerquest.org/cancer-biology/cancer-genes
search_genes = {
    "GOF": [
        'ABL1', 'AFF4', 'AKAP13', 'AKT2', 'ALK', 'AML1',
        'AXL', 'BCL-2', 'BCL-3', 'BCL-6', 'BCR', 'CAN',
        'CBFB', 'CCND1', 'CSF1R', 'DEK', 'E2A', 'EGFR', 
        'ERBB2', 'ERG', 'ETS1', 'EWSR1', 'FES', 'FGF3',
        'FGF4', 'FLI1', 'FOS', 'FUS', 'GLI1', 'GNAS', 
        'HER2', 'HRAS', 'IL3', 'JUN', 'K-SAM', 'KIT', 
        'KRAS', 'LCK', 'LMO1', 'LMO2', 'LYL1','MAS1', 
        'MCF2', 'MDM2', 'MLLT11', 'MOS', 'MTG8', 'MYB', 
        'MYC', 'MYCN', 'MYH11', 'NEU', 'NFKB2', 'NOTCH1', 
        'NPM', 'NRAS', 'NRG', 'NTRK1', 'NUP214', 'PAX-5', 
        'PBX1', 'PIM1', 'PML', 'RAF1', 'RARA', 'REL', 
        'RET', 'RHOM1', 'RHOM2', 'ROS1', 'RUNX1', 'SET', 
        'SIS', 'SKI', 'SRC', 'TAL1', 'TAL2', 'TCF3', 
        'TIAM1', 'TLX1', 'TSC2'
    ],
    "LOF": [
        'APC', 'BRCA1', 'BRCA2', 'CDKN2A', 'DCC', 
        'DPC4', 'MADR2', 'MEN1', 'NF1', 'NF2', 'PTEN', 
        'RB1', 'TP53', 'VHL', 'WRN', 'WT1'
    ]
}

pubmed = PubMed(tool="GeneSearcher", email="hugh.warden@outlook.com")

data = pd.DataFrame(
    columns=[
        'pubmed_id',
        'title',
        'abstract',
        'gene',
        'gene_type',
        'keywords',
        'journal',
        'conclusions',
        'methods',
        'results',
        'copyrights',
        'doi',
        'publication_date',
        'authors'
    ]
)

for gene_type in search_genes.keys():
    for gene in search_genes[gene_type]:
        results = pubmed.query(gene, max_results=500)
        articleList = []
        articleInfo = []
        for article in results:
            articleDict = article.toDict()
            articleList.append(articleDict)
        for article in articleList:
            pubmedId = article['pubmed_id'].partition('\n')[0]
            articleInfo.append({u'pubmed_id':pubmedId,
                            u'title':article['title'],
                            u'abstract':article['abstract'],
                            u'gene':gene,
                            u'gene_type':gene_type,
                            #u'keywords':article['keywords'],
                            #u'journal':article['journal'],
                            #u'conclusions':article['conclusions'],
                            #u'methods':article['methods'],
                            #u'results': article['results'],
                            #u'copyrights':article['copyrights'],
                            #u'doi':article['doi'],
                            #u'publication_date':article['publication_date'], 
                            #'authors':article['authors']
                        })
        appendPD = pd.DataFrame.from_dict(articleInfo)
        data = data.append(appendPD)
        
data.to_csv(
    "data/mutation-abstracts.csv", 
    sep="\t",
    index=False
)
