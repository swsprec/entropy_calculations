import sys
import os
import argparse
import json
import collections 
import math

def parse_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, 
                        help="folder containing files to run entropy check on", 
                        dest="in_folder")
    parser.add_argument('-o', '--output', required=True, 
                        help="file to write final statistics to, JSON", 
                        dest="output_file")
    return parser.parse_args()


def shannon_entropy(file_name):
    # read the whole file into a byte array
    with open(file_name, "rb") as f:
        byteArr = map(ord, f.read())

    fileSize = len(byteArr)
    
    # calculate the frequency of each byte value in the file
    freqList = [0]*256
    for pos, val in enumerate(freqList):
        freqList[pos] = float(byteArr.count(pos)) / fileSize

    # Shannon entropy
    ent = 0.0
    for freq in freqList:
        if freq > 0:
            ent = ent + freq * math.log(freq, 2)
    ent = -ent
    return ent, fileSize


def encryption_numbers(file_name):
    openssl_enc_methods = ["-aes256", "-blowfish", "-chacha", "-RC4"]
    password = "infected"
    
    entropies = []

    for method in openssl_enc_methods:
        command = "openssl enc %s -in '%s' -pass pass:%s > tmp" % (method, file_name, password)
        os.system(command)
        entropies.append(shannon_entropy("tmp")[0])
       
    return entropies

def compression_numbers(file_name):
    entropies = []

    command1 = "bzip2 -kzf '%s'" % file_name
    os.system(command1)
    outfile = "%s.bz2" % file_name
    entropies.append(shannon_entropy(outfile)[0])
    os.system("rm '%s'" % outfile)

    command2 = "gzip -kf '%s'" % file_name
    os.system(command2)
    outfile = "%s.gz" % file_name
    entropies.append(shannon_entropy(outfile)[0])
    os.system("rm '%s'" % outfile)

    command3 = "7z a tmp '%s' > /dev/null" % file_name
    os.system(command3)
    outfile = "tmp.7z"
    entropies.append(shannon_entropy(outfile)[0])
    os.system("rm %s" % outfile)
       
    command4 = "xz -kzf '%s'" % file_name
    os.system(command4)
    outfile = "%s.xz" % file_name
    entropies.append(shannon_entropy(outfile)[0])
    os.system("rm '%s'" % outfile)

    return entropies



def main():
    args = parse_cmd()
    
    in_folder = args.in_folder
    stats_file = args.output_file

    assert os.path.exists(in_folder), "I did not find the folder at, "+str(in_folder)

    with open(stats_file, "w") as stats_out:

        csv_headers = "filename,size (in bytes),file extension,base shannon entropy,"\
                        "aes256,blowfish,chacha,rc4,"\
                        "bzip2,gzip,7zip,xz"
        stats_out.write("%s\n" % csv_headers)
    
        for file in os.listdir(in_folder):
            file_and_path = "%s/%s" % (in_folder, file)
            extension = ".".join(file.split(".")[1:])
            
    
            try:
    
                print("base shannon for %s" % file_and_path)
                # get shannon entropy of base file
                base_ent, fileSize = shannon_entropy(file_and_path)
                
                print("compress shannon %s" % file_and_path)
                # get shannon entropy of compressed file
                comp_ent = compression_numbers(file_and_path)


                print("encrypt shannon %s" % file_and_path)
                # get shannon entropy of encrypted file
                enc_ent = encryption_numbers(file_and_path)

                
                output = "%s,%s,%s,%f,%s,%s\n" % (file, fileSize,extension, 
                                                base_ent, 
                                                str(enc_ent).strip("[]").replace(" ", ''),
                                                str(comp_ent).strip("[]").replace(" ", ''))
                print("finished %s" % file_and_path)
                stats_out.write(output)
            except:
                print("Error with file: %s, moving on" % file_and_path)
                continue

if __name__ == "__main__":
    main()
