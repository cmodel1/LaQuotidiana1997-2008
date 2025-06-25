import csv
import xml.etree.ElementTree as ET
import os
from constants import CONFIGS, SORTED_RAW_DATA_DIR, XML_NS 

def parse_xml_file(xmlFile, year):
    print(f"Parsing XML file: {xmlFile}")
    tree = ET.parse(xmlFile)
    root = tree.getroot()

    articles = {"rm-vallader": [], "rm-surmiran": [], "rm-sursilv":[], "rm-rumgr":[], "rm-puter":[], "rm-sutsilv":[]}

    for doc in root.iter('DOC'):
        lang = doc.get(f"{{{XML_NS}}}lang")
        articles[lang].append({"id": doc.attrib["id"], "year": year, "type": doc.attrib["type"], "lang": lang, "text": []})
        for p in doc.iter("P"):
            articles[lang][-1]["text"].append(p.text)

        # if doc.get(f"{{{XML_NS}}}lang") == "rm-vallader":
        #     articles["rm-vallader"].append({"id": doc.attrib["id"], "type": doc.attrib["type"], "lang": doc.get(f"{{{XML_NS}}}lang"), "text": []})
        #     for p in doc.iter("P"):
        #         articles["rm-vallader"][-1]["text"].append(p.text)

        # elif doc.get(f"{{{XML_NS}}}lang") == "rm-surmiran":
        #     articles["rm-surmiran"].append({"id": doc.attrib["id"], "type": doc.attrib["type"], "lang": doc.get(f"{{{XML_NS}}}lang"), "text": []})
        #     for p in doc.iter("P"):
        #         articles["rm-surmiran"][-1]["text"].append(p.text)

        # elif doc.get(f"{{{XML_NS}}}lang") == "rm-sursilv":
        #     articles["rm-sursilv"].append({"id": doc.attrib["id"], "type": doc.attrib["type"], "lang": doc.get(f"{{{XML_NS}}}lang"), "text": []})
        #     for p in doc.iter("P"):
        #         articles["rm-sursilv"][-1]["text"].append(p.text)

        # elif doc.get(f"{{{XML_NS}}}lang") == "rm-rumgr":
        #     articles["rm-rumgr"].append({"id": doc.attrib["id"], "type": doc.attrib["type"], "lang": doc.get(f"{{{XML_NS}}}lang"), "text": []})
        #     for p in doc.iter("P"):
        #         articles["rm-rumgr"][-1]["text"].append(p.text)

        # elif doc.get(f"{{{XML_NS}}}lang") == "rm-puter":
        #     articles["rm-puter"].append({"id": doc.attrib["id"], "type": doc.attrib["type"], "lang": doc.get(f"{{{XML_NS}}}lang"), "text": []})
        #     for p in doc.iter("P"):
        #         articles["rm-puter"][-1]["text"].append(p.text)

        # elif doc.get(f"{{{XML_NS}}}lang") == "rm-sutsilv":
        #     articles["rm-sutsilv"].append({"id": doc.attrib["id"], "type": doc.attrib["type"], "lang": doc.get(f"{{{XML_NS}}}lang"), "text": []})
        #     for p in doc.iter("P"):
        #         articles["rm-sutsilv"][-1]["text"].append(p.text)
        
    print(f"Parsed {len(articles['rm-vallader'])} Vallader, {len(articles['rm-surmiran'])} Surmiran, {len(articles['rm-sursilv'])} Sursilv, {len(articles['rm-rumgr'])} Rumantsch Grischun, {len(articles['rm-puter'])} Puter, {len(articles['rm-sutsilv'])} Sutsilv articles")
    return articles

def save_articles_to_tsv(articles):
    os.makedirs(SORTED_RAW_DATA_DIR, exist_ok=True)

    for lang, article_list in articles.items():
        path = f"{SORTED_RAW_DATA_DIR}/{lang}_articles.tsv"

        with open(path, "a", newline="", encoding="utf-8") as tsvfile:
            writer = csv.writer(tsvfile, delimiter="\t")

            for article in article_list:
                clean_text = " ".join(article["text"]).replace("\n", " ").strip()
                writer.writerow([
                    article["id"],
                    article["year"],
                    article["type"],
                    article["lang"],
                    clean_text
                ])

def main():
    # Remove existing tsv files to avoid duplicates and create new ones
    print("Sorting all La Quotidiana articles in the la_quotidiana/ directory by idiom in the {SORTED_RAW_DATA_DIR}/ directory.\n")
    print("Removing existing idiom tsv files from the {SORTED_RAW_DATA_DIR}/ directory.\n")
    for lang in CONFIGS:
        if os.path.exists(f"{SORTED_RAW_DATA_DIR}/{lang}_articles.tsv"):
            os.remove(f"{SORTED_RAW_DATA_DIR}/{lang}_articles.tsv")
            with open(f"{SORTED_RAW_DATA_DIR}/{lang}_articles.tsv", "w", encoding="utf-8") as f:
                f.write("id\tyear\ttype\tlang\ttext\n")
    
    # Sort all articles across the La Quotidiana files into their respctive idiom tsv file
    for i in range(1997, 2009):
        articles = parse_xml_file(f"la_quotidiana/rm_quotidiana_{i}.xml", i)
        print(f"Sorting all articles from {i} by idiom.\n")
        save_articles_to_tsv(articles)
    
    print(f"All articles sorted by idiom and saved to the {SORTED_RAW_DATA_DIR}/ directory.")


if __name__ == "__main__":
    main()