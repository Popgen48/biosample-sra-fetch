import sys
import re

#usage python extract_info.py Bos_taurus_ncbi_biosample.txt Braunvieh

tsv_in = sys.argv[1]
breed_name = sys.argv[2]

file_o = open(f"{breed_name}_biosample.txt","w")

##breed name can be present in any of the following field
##breed-->   /breed="Belgian blue"
##strain--> /strain="Belgian Blue"
##record_start --> 580: Belgian Blue
##after info --> BelgianBluexHolstein


record_list = []
first_record = True
write_record = False
with open(tsv_in) as source:
    for line in source:
        if not line.startswith(" "):
            match = re.match('[0-9]+:',line)
            if match:
                if not first_record:
                    for record in record_list:
                        if "BioSample" in record and "Identifiers:" in record:
                            pattern = re.compile('BioSample:([^;]+)')
                            match = re.findall(pattern,record)
                            biosample = match[0].lstrip()
                        if breed_name in record or breed_name.capitalize() in record:
                            write_record = True
                            w_record = record ##important to write the line with breed name to make sure that it refers to the breed only 
                if write_record:
                    file_o.write(f"{biosample} {w_record}\n")
                del record_list[:]
                first_record = False
                write_record = False
        record_list.append(line.rstrip().lstrip())
file_o.close()
