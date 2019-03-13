import math
import sys
from scipy import stats, special
import numpy
import binascii


'''
Code via for serial(): https://gist.github.com/StuartGordonReid/a4b1bc69bb52bb9343fa
'''
def serial(bin_data, pattern_length=16, method="first"):
    """
    Note that this description is taken from the NIST documentation [1]
    [1] http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf
    The focus of this test is the frequency of all possible overlapping m-bit patterns across the entire
    sequence. The purpose of this test is to determine whether the number of occurrences of the 2m m-bit
    overlapping patterns is approximately the same as would be expected for a random sequence. Random
    sequences have uniformity; that is, every m-bit pattern has the same chance of appearing as every other
    m-bit pattern. Note that for m = 1, the Serial test is equivalent to the Frequency test of Section 2.1.
    :param bin_data: a binary string
    :param pattern_length: the length of the pattern (m)
    :return: the P value
    """
    n = len(bin_data)
    # Add first m-1 bits to the end
    bin_data += bin_data[:pattern_length - 1:]

    # Get max length one patterns for m, m-1, m-2
    max_pattern = ''
    for i in range(pattern_length + 1):
        max_pattern += '1'

    # Keep track of each pattern's frequency (how often it appears)
    vobs_one = numpy.zeros(int(max_pattern[0:pattern_length:], 2) + 1)
    vobs_two = numpy.zeros(int(max_pattern[0:pattern_length-1:], 2) + 1)
    vobs_thr = numpy.zeros(int(max_pattern[0:pattern_length-2:], 2) + 1)

    for i in range(n):
        # Work out what pattern is observed
        vobs_one[int(bin_data[i:i + pattern_length:], 2)] += 1
        vobs_two[int(bin_data[i:i + pattern_length-1:], 2)] += 1
        vobs_thr[int(bin_data[i:i + pattern_length-2:], 2)] += 1

    vobs = [vobs_one, vobs_two, vobs_thr]
    sums = numpy.zeros(3)
    for i in range(3):
        for j in range(len(vobs[i])):
            sums[i] += pow(vobs[i][j], 2)
        sums[i] = (sums[i] * pow(2, pattern_length-i)/n) - n

    # Calculate the test statistics and p values
    del1 = sums[0] - sums[1]
    del2 = sums[0] - 2.0 * sums[1] + sums[2]
    p_val_one = special.gammaincc(pow(2, pattern_length-1)/2, del1/2.0)
    p_val_two = special.gammaincc(pow(2, pattern_length-2)/2, del2/2.0)

    # For checking the outputs
    if method == "first":
        return p_val_one
    else:
        # I am not sure if this is correct, but it makes sense to me.
        return min(p_val_one, p_val_two)




def get_bytes_from_file(filename):  
    x = open(filename, "rb").read()
    return x

def get_obs_freq(byte_arr):
    observed = [0] * 256
    true_byte_arr = []
    bin_string =''
    mean = 0.0
    for byte in byte_arr:
        actual_byte = ord(byte)
        bits = bin(actual_byte)[2:]
        bin_string += bits.zfill(8*((len(bits) + 7) // 8))
        mean += actual_byte
        observed[actual_byte] += 1
        true_byte_arr.append(actual_byte)
    mean /= len(true_byte_arr)
    return observed, true_byte_arr, mean, bin_string

def main():
    byte_arr = get_bytes_from_file(sys.argv[1])

    observed, byte_arr, mean, bin_arr = get_obs_freq(byte_arr)
    expected = [len(byte_arr) / 256.0] * 256
    degrees_of_freedom = 255

    serial_c = serial(bin_arr,pattern_length=8)


    chi_square = stats.chisquare(observed, f_exp=expected)[0]
    prob = stats.chisqprob(chi_square, degrees_of_freedom)

    if(serial_c >= 0.01):
        print("Encryption")
    else:
        print("Other")

    print("File_name,chi-square,chi-square-probability,mean_byte,serial_correlation_p-value")

    print("%s,%f,%f,%f,%f" % (sys.argv[1], chi_square, prob, mean, serial_c))



if __name__ == "__main__":
    main()
