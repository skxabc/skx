/*test function*/

#include <stdio.h>
#if !defined WIN32 && !defined _WIN32
#include <unistd.h>
#endif

#include <stdlib.h>
#include "myspeex.h"

#define BUFFER_SIZE 2000

/*
This is the main test function for speex

INPUT:
		int argc
		char **argv
OUTPUT:

HISTORY:
		Version No.  Author         Remarks
		v01       Yongtao Sha    Created on 2016-10-23
*/
int main(int argc, char **argv)
{
	//test part
	char *inFile, *bitsFile, *outFile; //file name
	FILE *fin = NULL, *fbits = NULL, *fout = NULL;//file pointer

	//user part
	int result;
	void *enc_st;//encoder state
	void *dec_st;//decoder state
	short input_buf[BUFFER_SIZE];//input data buffer
	int input_len = 320;//input data length	
	char *cbits = NULL;
	int cbits_len;
	short *output_buf = NULL;
	int output_len;
	//int flag = 1;

   if (argc != 4)
   {
      fprintf (stderr, "Usage: [in file] [encoder bits] [decoder out file]\n argc = %d", argc);
      exit(1);
   }
   inFile = argv[1];
   fin = fopen(inFile, "rb");
   bitsFile = argv[2];
   fbits = fopen(bitsFile, "wb");
   outFile = argv[3];
   fout = fopen(outFile, "wb+");

      
   //encoder open
   result = enc_open_func(&enc_st);
   if (result != 0)
   {
	   return result;
   }

   //decoder open
   result = dec_open_func(&dec_st);
   if (result != 0)
   {
	   return result;
   }

   while (!feof(fin))
   {
	   fread(input_buf, sizeof(short), input_len, fin);
	   if (feof(fin))
		   break;
	   
	   //encoder process
	   cbits_len = enc_process_func(enc_st, input_buf, input_len, &cbits);
	   if (cbits_len < 0)
	   {
		   return cbits_len;
	   }

	   //write encoder bits to file
	   fwrite(cbits, sizeof(char), cbits_len, fbits);

	   //decoder process
	   output_len = dec_process_func(dec_st, cbits, cbits_len, &output_buf);
	   if (output_len < 0)
	   {
		   return output_len;
	   }

	   //write decoder data to file
	   fwrite(output_buf, sizeof(short), output_len, fout);

	   //input_len = input_len + flag * 320;

	   //flag = -flag;

   }

   //encoder close
   enc_close_func(enc_st);

   //decoder close
   dec_close_func(dec_st);

   //close file
   fclose(fin);
   fclose(fbits);
   fclose(fout);

   return 0;

}
