#!/usr/bin/env python3
import os


# http://www.uniprot.org/uniprot/?query=proteome:UP000005426&force=no&limit=no&format=fasta
def get_proteomes():
    proteoom_list = {}
    JGI_connect()
    # Aspergillus clavatus
    proteoom_list[
        "asp-cl"] = "http://www.uniprot.org/uniprot/?query=proteome:UP000006701&force=no&limit=no&format=fasta"
    # Aspergillus(of Emericella) nidulans
    proteoom_list[
        "eme-ni"] = "http://www.uniprot.org/uniprot/?query=proteome:UP000000560&force=no&limit=no&format=fasta"
    # Aspergillus niger
    proteoom_list[">asp-ni"] = download_JGI_proteome("Aspni7")
    # Heterogastridium pycnidioideum
    proteoom_list[">het-py"] = download_JGI_proteome("Hetpy1")
    # Magnaporthe grisea
    proteoom_list[
        "mag-gr"] = "http://www.uniprot.org/uniprot/?query=proteome:UP000009058&force=no&limit=no&format=fasta"
    # Penicillium bilaiae
    proteoom_list[">pen-bi"] = download_JGI_proteome("Penbi1")
    # Penicillium brevicompactum
    proteoom_list[">pen-br"] = download_JGI_proteome("Penbr2")
    # Phanerochaete chrysosporium
    proteoom_list[">pha-ch"] = download_JGI_proteome("Phchr2")
    # Rhizoctonia solani
    proteoom_list[
        "rhi-so"] = "http://www.uniprot.org/uniprot/?query=proteome:UP000044841&force=no&limit=no&format=fasta"
    # Saccharomyces cerevisiae
    proteoom_list[
        "sac-ce"] = "http://www.uniprot.org/uniprot/?query=proteome:UP000002311&force=no&limit=no&format=fasta"


    return (proteoom_list, proteoom_list.keys())

def check_db_exist(orglist):
    files_exist = True
    for x in orglist:
        if x[0] == ">":
            test = x[1:]
        else:
            test = x
        if (not os.path.exists("prot/" + test + ".fa") or
            not os.path.exists("prot/" + test + ".fa.phr") or
            not os.path.exists("prot/" + test + ".fa.pin") or
            not os.path.exists("prot/" + test + ".fa.psd") or
            not os.path.exists("prot/" + test + ".fa.psi") or
            not os.path.exists("prot/" + test + ".fa.psq")):
            files_exist = False
    if files_exist:
        if input("db files found, redownload?(y/n): ") == "y":
            return(False)
        else:
            return(True)
    return(False)

def JGI_connect():
    log("logging in to JGI")
    os.system("curl 'https://signon.jgi.doe.gov/signon/create' --data-urlencode 'login=sven@debijleveldjes.nl'" +
              " --data-urlencode 'password=bpcogs1617' -c cookies > /dev/null")


def download_JGI_proteome(org):
    log("donwloading file list of {}".format(org))
    os.system(
        "curl -s 'http://genome.jgi.doe.gov/ext-api/downloads/get-directory?organism=" + org + "' -b cookies > files.xml")
    file = open("files.xml", "r")
    directory = file.readlines()
    subdir = []
    for line in directory:
        if "all_proteins" in line and not "Filtered" in line:
            subdir.append(line)
    # print("~~~~subdir has", len(subdir), "items~~~~")
    if len(subdir) == 1:
        path = subdir[0].split("url=\"")[1].split("\"")[0]
        return ("http://genome.jgi.doe.gov" + path)
    elif len(subdir) == 0:
        log("could not find a donwload!!!!")
        log("trying to find a different donwload")
        second_test = []
        for x in directory:
            if "protein" in x and "aa" in x and int(x.split("size=\"")[1].split()[0]) < 100:
                log("found another download")
                second_test.append(x)
                log(x)
        if len(second_test) != 0:
            return("http://genome.jgi.doe.gov" + second_test[0].split("url=\"")[1].split("\"")[0])
        else:
            log("could not find any file with the names portein and filtered")
            return("error")
    else:
        log("there are multiple downloads!!!!")
        log("Downloads:")
        for x in subdir:
            log(x)
        log("choosing first flle for donwload")
        path = subdir[0].split("url=\"")[1].split("\"")[0]
        return ("http://genome.jgi.doe.gov" + path)


def download_proteomes(proteoom_lijst, org_lijst):
    for x in proteoom_lijst:
        # print(x, proteoom_lijst[x])
        if x[0] != ">":
            log("Downloading proteome for {}".format(x))
            os.system("wget \"" + proteoom_lijst[x] + "\" -O $(pwd)/prot/" + x + ".fa")
        else:
            log("Downloading proteome for {}".format(x[1:]))
            os.system("curl '" + proteoom_lijst[x] + "' -b cookies > $(pwd)/prot/" + x[1:] + ".fa.gz")
    for x in org_lijst:
        if x[0] == ">":
            os.system("gunzip $(pwd)/prot/" + x[1:] + ".fa.gz")
    for x in org_lijst:
        if x[0] == ">":
            os.system("cat {}.fa | awk -F"|" '{if (substr($0, 1, 1) == ">"){print ">"$3}else{print $0}}' > {}_temp.fa".format(x[1:], x[1:]))
            os.system("cat {}_temp.fa > {}.fa".format(x[1:], x[1:]))
            os.system("rm {}_temp.fa".format(x[1:]))


def make_databases(org_lijst):
    for x in org_lijst:
        log("making protein db for {}".format(x))
        os.system("makeblastdb -in $(pwd)/prot/" + x + ".fa -parse_seqids -dbtype prot")

def log(text):
    print("==LOG==", text)
    file = open("log.txt", "a")
    file.write(text + "\n")




def blasts(org_lijst):
    # x = .fa & y = db
    total = len(org_lijst) * (len(org_lijst) - 1)
    os.system("rm -rf blasts")
    os.system("mkdir blasts -p")
    log("~~~~blast")
    current = 0
    org_lijst2 = ["pha-ch", "mag-gr", "asp-cl", "pen-bi", "rhi-so"]
    for x in range(len(org_lijst2)):
        for y in range(len(org_lijst)):
            if x != y:
                if current == 0:
                    log ("~~blasting {} tegen de database van {} voortgang: 0.00 %".format(org_lijst[x], org_lijst[y]))
                else:
                    log("~~blasting {} tegen de database van {} voortgang: {} %".format(org_lijst[x], org_lijst[y], round(((current + 1)/total) * 100, 2)))
                #os.system("screen -S " + org_lijst[x] + "_" + org_lijst[y] + " -m bash blast2 -p blastp -d $(pwd)/prot/" + org_lijst[y] + ".fa -i $(pwd)/prot/" + org_lijst[
                    #x] + ".fa -m 8 -N -b 1 > $(pwd)/blasts/" + org_lijst[y] + ":" + org_lijst[x])
                os.system("blastall -p blastp -d $(pwd)/prot/" + org_lijst[y] + ".fa -i $(pwd)/prot/" + org_lijst[
                          x] + ".fa -m 8 -b 1 > $(pwd)/blasts/" + org_lijst[y] + ":" + org_lijst[x])
                current += 1


def main():
    os.system("rm -rf prot")
    os.system("mkdir prot -p")
    log_file = open("log.txt", "w")
    log_file.close()
    proteoom_lijst, org_lijst = get_proteomes()
    new_org_lijst = []
    for x in org_lijst:
        if x[0] == ">":
            new_org_lijst.append(x[1:])
        else:
            new_org_lijst.append(x)
    if not check_db_exist(org_lijst):
        log("downloads used for all organisms")
        for x in proteoom_lijst:
            log("{}\t\t{}".format(x, proteoom_lijst[x]))
        download_proteomes(proteoom_lijst, org_lijst)
        make_databases(new_org_lijst)
    blasts(new_org_lijst)


main()


# blast2 -p blastp -d UP000000560_227321.fasta -i UP000000591_284811.fasta -m 8 -N -b 1
