

#ifndef MYSPEEX_H
#define MYSPEEX_H

#define FRAME_SIZE 320 //frame size: Sampling rate:16kHz frame length:20ms
#define CBITS_SIZE 70

typedef struct enc_param
{
	int Fs; //Sampling rate: Narrowband (8 kHz),Wideband (16 kHz),\"Ultra-wideband\" (32 kHz), please set
	int quality;//Encoding quality (0-10), 0-lowest audio quality and lowest bitrate, 10-highest audio quality and highest bitrate, please set
	int bitrate;//encoding bit rate, similar as the quality, set to 0 is OK.
	int vbr_enabled;//Enable variable bit-rate (VBR)
	int vbr_max_bitrate; //max VBR bit-rate allowed
	float vbr_quality;//vbr_quality
	int abr_enabled;//Enable average bit-rate (ABR) at rate bps
	int vad_enabled;//Enable voice activity detection (VAD)
	int dtx_enabled;//Enable file-based discontinuous transmission (DTX)	
	int complexity;//Set encoding complexity (0-10), default 3
	int highpass_enabled;//Set the high-pass filter on (1) or off (0), default is on					 
	//int quiet;//
	//int lsb;//Raw input is little-endian(1) or big-endian(0)
	//int fmt;//Raw input is 8-bit unsigned(8) or 16-bit signed(16)
	//int nframes;//Number of frames per Ogg packet (1-10), default 1
	//int denoise_enabled;// Denoise the input before encoding
	//int agc_enabled;// Apply adaptive gain control (AGC) before encoding
	//int with_skeleton;//Outputs ogg skeleton metadata (may cause incompatibilities)
	//int chan; //Consider raw input as mono(1) or stereo(2)
	//int rate;// Sampling rate for raw input
	//int version;
	//int version_short;
	//int comment;
	//int author;
	//int title;
	//int print_rate;//Print the bitrate for each frame to standard output
} enc_para;

typedef struct dec_param
{
	int Fs;  //Sampling rate: Narrowband (8 kHz),Wideband (16 kHz),\"Ultra-wideband\" (32 kHz), please set
	int enh_enabled;//enable post-filter (default 1) 
	//int quiet;//default 0
	//int forceMode;//Force decoding in narrowband(0),wideband(1),ultra-wideband(2), default -1
	//int channels;//Force decoding in mono(1),stereo(2), default 1
	//int loss_percent;//Simulate n % random packet loss, default -1
} dec_para;

typedef struct state_enc_
{
	void *codec_st;
	void *bits;
	void *cbits;
	short pHisBuf[FRAME_SIZE];//zouying add 20171110
	int Bits_buf_len;//the len of output buffer malloced by the programme
	int HisLen;//zouying add 20171110
} state_enc;

typedef struct state_dec_
{
	void *codec_st;
	void *bits;
	void *output_data;
	int output_buf_len;
} state_dec;

int enc_open_func(state_enc **enc);

int enc_process_func(void *enc, short *input_buf, int input_len, char **cbits);

void enc_close_func(void *enc);

void enc_reset(void *enc);

int dec_open_func(state_dec **dec);

int dec_process_func(void *dec, char *cbits, int cbits_len, short **output_buf);

void dec_close_func(void *dec);

#endif
