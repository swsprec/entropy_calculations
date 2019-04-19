//
//  main.cpp
//  serial_correlation_test
//
//  Created by Steven Sprecher on 4/10/19.
//  Copyright © 2019 Steve Sprecher. All rights reserved.
//

#include <iostream>
#include <string>
#include <vector>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <unistd.h>
#include <fstream>
#include <typeinfo>
#include <cmath>
#include <boost/math/special_functions/gamma.hpp>

using namespace std;

static void show_usage(string name){
    cerr << "Usage: " << name << " INPUT_FILE" << endl;
}


double serial(string binary_data, int pattern) {
    
    return 0.0;
}

char* readFileBytes(const char *name)
{
    ifstream fl(name);
    fl.seekg( 0, ios::end );
    size_t len = fl.tellg();
    //char *ret = new char[len];
    char *ret = (char*)malloc(len);
    fl.seekg(0, ios::beg);
    fl.read(ret, len);
    fl.close();
    return ret;
}

static string Read(istream &stream){
    uint32_t count = 100;
    string result(count, ' ');
    stream.read(&result[0], count);
    return result;
}



void get_observed(double *vobs_one, double *vobs_two, double *vobs_three, string binary){
    
    unsigned long eight_bits = bitset<8>(binary).to_ulong();
    unsigned long seven_bits = bitset<7>(binary).to_ulong();
    unsigned long six_bits = bitset<6>(binary).to_ulong();
    
    vobs_one[eight_bits]++;
    vobs_two[seven_bits]++;
    vobs_three[six_bits]++;
    
}




int main(int argc, const char * argv[]) {
    
    if (argc != 2) {
        show_usage(argv[0]);
        exit(1);
    }
    
    cout << "Testing: " << argv[1] << endl;
    
    double vobs_one[256] = { 0 };
    double vobs_two[128] = { 0 };
    double vobs_three[64] = { 0 };
    long long NUM_BITS = 0;


    ifstream input;
    input.open(argv[1], ios::binary | ios::in);


    char char1;
    input.read(&char1, 1);
    int int1 = (int)(unsigned char)char1;


    NUM_BITS += 8;
    
    string binary = bitset<8>(int1).to_string();

    get_observed(vobs_one, vobs_two, vobs_three, binary);
    
    string combined,binary2;
    char char2;
    int int2;
    
    int counter = 0;
    
    while (input.good()) {
        input.read(&char2, 1);
        int2 = (int)(unsigned char)char2;
        NUM_BITS += 8;
        binary2 = bitset<8>(int2).to_string();
        combined = binary + binary2;
        for(int i = 1; i < combined.length(); ++i){
            string work = combined.substr(i,8);
            if(work.length() != 8){
                binary = binary2;
                break;
            }
            get_observed(vobs_one, vobs_two, vobs_three, work);
        }
        counter++;
    }
    
//    I now have the observed frequencies and such, now need to do the stats and sums and the like
    long double sums[3] = {0.0,0.0,0.0};
    
    for(int i = 0; i < 256; ++i){
        sums[0] += pow(vobs_one[i],2);
    }
    sums[0] = (sums[0] * pow(2, 8)/NUM_BITS) - NUM_BITS;


    for(int j = 0; j < 128; ++j){
        sums[1] += pow(vobs_two[j],2);
    }
    sums[1] = (sums[1] * pow(2, 7)/NUM_BITS) - NUM_BITS;


    for(int q = 0; q < 64; ++q){
        sums[2] += pow(vobs_three[q],2);
    }
    sums[2] = (sums[2] * pow(2, 6)/NUM_BITS) - NUM_BITS;




//    for(int i = 0; i < 3; ++i){
//        int num_elements;
//        (*vobs[i]).size();
//        for(int j = 0; j < vobs[i] / 8; ++j){
//            sums[i] += pow(vobs[i][j],2);
//        }
//        sums[i] = (sums[i] * (pow(2,8 - i)/NUM_BITS)) - NUM_BITS;
//    }
    
    long double del1 = sums[0] - sums[1];

    long double arg1 = 64;
    long double arg2 = del1 / 2;

    long double p_value = boost::math::gamma_q(arg1, arg2);


    if (p_value >= .01){
        cout << "Encryption" << endl;
    }
    else{
        cout << "Not Encryption" << endl;
    }

    cout << p_value << endl;

    return 0;
}
