/* The Computer Language Benchmarks Game
 * http://benchmarksgame.alioth.debian.org/
 *
 * by Paul Hsieh
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>       
#include <sys/types.h>
#include <unistd.h>

#include "time.h"

#define IM 139968
#define IA   3877
#define IC  29573

double gen_random (double max) {
    static long last = 42;
    return max * (last = (last * IA + IC) % IM) / IM;
}

struct aminoacids {
    char c;
    double p;
};

/* Weighted selection from alphabet */

void makeCumulative (struct aminoacids * genelist, int count) {
    double cp = 0.0;
    int i;

    for (i=0; i < count; i++) {
        cp += genelist[i].p;
        genelist[i].p = cp;
    }
}

char selectRandom (const struct aminoacids * genelist, int count) {
    double r = gen_random (1);
    int i, lo, hi;

    if (r < genelist[0].p) return genelist[0].c;

    lo = 0;
    hi = count-1;

    while (hi > lo+1) {
        i = (hi + lo) / 2;
        if (r < genelist[i].p) hi = i; else lo = i;
    }
    return genelist[hi].c;
}

/* Generate and write FASTA format */

#define LINE_LENGTH (60)

void makeRandomFasta (const char * id, const char * desc, const struct
aminoacids * genelist, int count, int n) {
   int todo = n;
   int i, m;

   printf (">%s %s\n", id, desc);

   for (; todo > 0; todo -= LINE_LENGTH) {
       char pick[LINE_LENGTH+1];
       if (todo < LINE_LENGTH) m = todo; else m = LINE_LENGTH;
       for (i=0; i < m; i++) pick[i] = selectRandom (genelist, count);
       pick[m] = '\0';
       puts (pick);
   }
}

void makeRepeatFasta (const char * id, const char * desc, const char *
s, int n) {
   char * ss;
   int todo = n, k = 0, kn = strlen (s);
   int m;

   ss = (char *) malloc (kn + 1);
   memcpy (ss, s, kn+1);

   printf (">%s %s\n", id, desc);

   for (; todo > 0; todo -= LINE_LENGTH) {
       if (todo < LINE_LENGTH) m = todo; else m = LINE_LENGTH;

       while (m >= kn - k) {
           printf ("%s", s+k);
           m -= kn - k;
           k = 0;
       }

       ss[k + m] = '\0';
       puts (ss+k);
       ss[k + m] = s[m+k];
       k += m;
   }

   free (ss);
}

/* Main -- define alphabets, make 3 fragments */

struct aminoacids iub[] = {
    { 'a', 0.27 },
    { 'c', 0.12 },
    { 'g', 0.12 },
    { 't', 0.27 },

    { 'B', 0.02 },
    { 'D', 0.02 },
    { 'H', 0.02 },
    { 'K', 0.02 },
    { 'M', 0.02 },
    { 'N', 0.02 },
    { 'R', 0.02 },
    { 'S', 0.02 },
    { 'V', 0.02 },
    { 'W', 0.02 },
    { 'Y', 0.02 }
};

#define IUB_LEN (sizeof (iub) / sizeof (struct aminoacids))

struct aminoacids homosapiens[] = {
    { 'a', 0.3029549426680 },
    { 'c', 0.1979883004921 },
    { 'g', 0.1975473066391 },
    { 't', 0.3015094502008 },
};

#define HOMOSAPIENS_LEN (sizeof (homosapiens) / sizeof (struct aminoacids))

char * alu =
   "GGCCGGGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGG" \
   "GAGGCCGAGGCGGGCGGATCACCTGAGGTCAGGAGTTCGAGA" \
   "CCAGCCTGGCCAACATGGTGAAACCCCGTCTCTACTAAAAAT" \
   "ACAAAAATTAGCCGGGCGTGGTGGCGCGCGCCTGTAATCCCA" \
   "GCTACTCGGGAGGCTGAGGCAGGAGAATCGCTTGAACCCGGG" \
   "AGGCGGAGGTTGCAGTGAGCCGAGATCGCGCCACTGCACTCC" \
   "AGCCTGGGCGACAGAGCGAGACTCCGTCTCAAAAA";

void run (int n) {
    clock_t t = clock();

    makeRepeatFasta ("ONE", "Homo sapiens alu", alu, n*2);
    makeRandomFasta ("TWO", "IUB ambiguity codes", iub, IUB_LEN, n*3);
    makeRandomFasta ("THREE", "Homo sapiens frequency", homosapiens, HOMOSAPIENS_LEN, n*5);

    fprintf(stderr, "time(%.2f)\n", (float)(clock() - t)/CLOCKS_PER_SEC);
}


int main(int argc, char* argv[])
{
  makeCumulative (iub, IUB_LEN);
  makeCumulative (homosapiens, HOMOSAPIENS_LEN);

  unsigned N = (argc > 1) ? atol(argv[1]) : 100;
  unsigned times = (argc > 2) ? atol(argv[2]) : 1;

  fprintf(stderr, "started\t%d\n", getpid());

  for (int i = 0; i < times; i++) { run(N); }

  return 0;
} /* main() */
