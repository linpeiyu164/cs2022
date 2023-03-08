// g++ test.cpp -lssl -lcrypto
// FLAG{I5_tH15_cHA1l3nGe_t0O_eA5Y_0R_tO0_HARD}
#include <stdio.h>
#include <openssl/evp.h>
#include <openssl/aes.h>

int main(){
    unsigned char in[] = "\xD2\xB2\x40\xF2\xDE\x77\xE0\x85\xFD\xE5\xBF\xB1\xEB\xF7\x64\x18\xE4\xAD\x85\xEF\x80\x68\xDA\x2C\x25\x2D\xE1\xF8\xDD\xE7\x0B\x59\xE8\xD7\x57\x37\x2F\xB5\x41\x25\x78\x5A\xB9\x82\x22\x8D\x81\x26";
    unsigned char iv[] = "\xB5\x9A\xEC\x92\x51\xE2\x5E\x3F\x90\x81\xE4\x27\x19\x2E\x50\x29";
    unsigned char key[] = "\x4B\x29\x47\x0F\x38\xD4\xA3\x4D\x1C\x9F\x4F\xC7\x74\xE4\x29\x6A";
    unsigned char * out = (unsigned char *)malloc(sizeof(in) * 2);
    int outl = sizeof(out) / sizeof(unsigned char);
    int inl = sizeof(in) / sizeof(unsigned char);

    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    EVP_CIPHER_CTX_init(ctx);
    EVP_DecryptInit(ctx, EVP_aes_128_cbc(), key, iv);
    EVP_DecryptUpdate(ctx, out, &outl, in, inl);
    printf("%s\n", out);
    EVP_DecryptFinal(ctx, out, &outl);
    EVP_CIPHER_CTX_free(ctx);
}