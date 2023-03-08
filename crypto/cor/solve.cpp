#include "iostream"
#include "vector"
#include "algorithm"
#include "string"
#include "assert.h"
#include "fstream"
using namespace std;

int output[] = {1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1};

class LFSR{
    public:
    unsigned long long state;
    vector<int> tap;
    int size;

    LFSR(unsigned long long init_state, int init_size, vector<int> init_tap){
        state = init_state;
        tap = init_tap;
        size = init_size;
    }

    int getbit(){
        int next = 0;
        for(auto val: tap){
            if(state & (1 << val)){
                next ^= 1;
            }
        }
        int out = state & 1;
        state = state >> 1;
        if(next){
            state = state | (1 << (size-1));
        }
        return out;
    }
};

void find_possible(int size, vector<int> tap, unsigned long long& possible, vector<int>& last){
    for(unsigned long long i = 0; i < (1ULL << size); i++){
        LFSR lfsr(i, size, tap);
        int count = 0;
        for(int j = 0; j < 200; j++){
            int cur = lfsr.getbit();
            if(cur == last[j]){
                count++;
            }
        }
        if(double(count) / 200 >= 0.7){
            cout << "number of counts: " << count << '\n';
            possible = i;
            cout << i << '\n';
        }
    }
}

void reverse_shift(LFSR& lfsr, vector<int> revtap, int size){
    int num = 0;
    int next = lfsr.state & (1 << (size - 1));
    for(auto val: revtap){
        if(lfsr.state & (1 << val)){
            num ^= 1;
        }
    }
    lfsr.state = lfsr.state << 1;
    lfsr.state = lfsr.state | num;
}

int main(){
    // copy the last 200
    vector<int> last(200, 0);
    for(int i = 232; i < 432; i++){
        last[i-232] = output[i];
    }

    vector<int> tap1 = {0, 13, 16, 26};
    vector<int> tap2 = {0, 5, 7, 22};
    vector<int> tap3 = {0, 17, 19, 24};

    vector<int> rev_tap1 = {12, 15, 25, 26};
    vector<int> rev_tap2 = {4, 6, 21, 22};
    vector<int> rev_tap3 = {16, 18, 23, 24};

    unsigned long long orig_state1;
    unsigned long long orig_state2;
    unsigned long long orig_state3;

    int size1 = 27;
    int size2 = 23;
    int size3 = 25;

    find_possible(size2, tap2, orig_state2, last);
    find_possible(size3, tap3, orig_state3, last);

    vector<int> output_2;
    vector<int> output_3;

    LFSR lfsr2(orig_state2, size2, tap2);
    LFSR lfsr3(orig_state3, size3, tap3);

    for(int i = 0; i < 200; i++){
        output_2.push_back(lfsr2.getbit());
        output_3.push_back(lfsr3.getbit());
    }

    for(unsigned long long st1 = 0; st1 < (1 << size1); st1++){
        LFSR lfsr1(st1, size1, tap1);
        int count = 0;
        for(int i = 0; i < 200; i++){
            int x1 = lfsr1.getbit();
            int out = x1 ? output_2[i] : output_3[i];
            if(out == last[i]){
                count++;
            }
        }
        if(count == 200){
            orig_state1 = st1;
            cout << orig_state1 << '\n';
            cout << orig_state2 << '\n';
            cout << orig_state3 << '\n';
        }
    }

    LFSR lfsr1_n(orig_state1, size1, tap1);
    LFSR lfsr2_n(orig_state2, size2, tap2);
    LFSR lfsr3_n(orig_state3, size3, tap3);

    for(int i = 0; i < 232; i++){
        reverse_shift(lfsr1_n, rev_tap1, size1);
        reverse_shift(lfsr2_n, rev_tap2, size2);
        reverse_shift(lfsr3_n, rev_tap3, size3);
    }

    vector<int> flag;
    for(int i = 0; i < 432; i++){
        int x1 = lfsr1_n.getbit();
        int x2 = lfsr2_n.getbit();
        int x3 = lfsr3_n.getbit();
        int x = x1 ? x2 : x3;
        flag.push_back(x ^ output[i]);
    }

    int count = 0;
    string flag_str = "";
    for(int i = 0; i < 232; i++){
        int val = flag[i] << (7 - (i % 8));
        count += val;
        if(i % 8 == 7){
            flag_str += char(count);
            count = 0;
        }
    }
    cout << flag_str;
}