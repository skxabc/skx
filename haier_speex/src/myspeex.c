
#include <stdlib.h>

#include "speex/speex.h"
#include "myspeex.h"
#include "os_support.h"

/* 
This is the open function for speex encoder

INPUT:
		void *enc:   encoder state
OUTPUT:
		void *enc:   encoder state

HISTORY:
		Version No.  Author         Remarks
		v01       Yongtao Sha    Created on 2016-11-2
*/
int enc_open_func(state_enc **enc)
{
	int modeID;
	const SpeexMode *mode = NULL;	
	int tmp;
	void *st;
	state_enc *penc;
	SpeexBits *pbits;

	enc_para input_para = //encoder parameter
	{
		16000, //Fs; //Sampling rate: Narrowband (8 kHz),Wideband (16 kHz),\"Ultra-wideband\" (32 kHz), please set
		8, // quality;//Encoding quality (0-10), 0-lowest audio quality and lowest bitrate, 10-highest audio quality and highest bitrate, please set
		0, // bitrate;//encoding bit rate, similar as the quality, set to 0 is OK.
		0, // vbr_enabled;//Enable variable bit-rate (VBR)
		0, // vbr_max_bitrate; //max VBR bit-rate allowed
		-1, // vbr_quality;//vbr_quality
		0, // abr_enabled;//Enable average bit-rate (ABR) at rate bps
		0, // vad_enabled;//Enable voice activity detection (VAD)
		0, // dtx_enabled;//Enable file-based discontinuous transmission (DTX)	
		3, // complexity;//Set encoding complexity (0-10), default 3
		1 // highpass_enabled;//Set the high-pass filter on (1) or off (0), default is on					 
		   //0, // quiet;//
		   //1, // lsb;//Raw input is little-endian(1) or big-endian(0)
		   //16, // fmt;//Raw input is 8-bit unsigned(8) or 16-bit signed(16)
		   //1, // nframes;//Number of frames per Ogg packet (1-10), default 1
		   //0, // denoise_enabled;// Denoise the input before encoding
		   //0, // agc_enabled;// Apply adaptive gain control (AGC) before encoding
		   //0, // with_skeleton;//Outputs ogg skeleton metadata (may cause incompatibilities)
		   //1, // chan; //Consider raw input as mono(1) or stereo(2)
		   //0, // rate;// Sampling rate for raw input
		   //int version;
		   //int version_short;
		   //int comment;
		   //int author;
		   //int title;
		   //0,  // print_rate;//Print the bitrate for each frame to standard output		   
	};

	if (input_para.Fs == 8000)
		modeID = SPEEX_MODEID_NB;
	else if (input_para.Fs == 16000)
		modeID = SPEEX_MODEID_WB;
	else if (input_para.Fs == 32000)
		modeID = SPEEX_MODEID_UWB;
	else
	{
		return -1;
		fprintf(stderr, "Error: sampling rate %d is not suitable, please try 8000, 16000 or 32000\n", input_para.Fs);
	}

	mode = speex_lib_get_mode(modeID);

	/*Initialize Speex encoder*/
    st = speex_encoder_init(mode);

	speex_encoder_ctl(st, SPEEX_SET_COMPLEXITY, &(input_para.complexity));
	speex_encoder_ctl(st, SPEEX_SET_SAMPLING_RATE, &(input_para.Fs));
	if (input_para.quality >= 0)
	{
		if (input_para.vbr_enabled)
		{
			if (input_para.vbr_max_bitrate>0)
				speex_encoder_ctl(st, SPEEX_SET_VBR_MAX_BITRATE, &(input_para.vbr_max_bitrate));
			speex_encoder_ctl(st, SPEEX_SET_VBR_QUALITY, &(input_para.vbr_quality));
		}
		else
			speex_encoder_ctl(st, SPEEX_SET_QUALITY, &(input_para.quality));
	}
	if (input_para.bitrate)
	{
		if (input_para.quality >= 0 && input_para.vbr_enabled)
			fprintf(stderr, "Warning: --bitrate option is overriding --quality\n");
		speex_encoder_ctl(st, SPEEX_SET_BITRATE, &(input_para.bitrate));
	}
	if (input_para.vbr_enabled)
	{
		tmp = 1;
		speex_encoder_ctl(st, SPEEX_SET_VBR, &tmp);
	}
	else if (input_para.vad_enabled)
	{
		tmp = 1;
		speex_encoder_ctl(st, SPEEX_SET_VAD, &tmp);
	}
	if (input_para.dtx_enabled)
	{
		tmp = 1;
		speex_encoder_ctl(st, SPEEX_SET_DTX, &tmp);
	}
	if (input_para.dtx_enabled && !(input_para.vbr_enabled || input_para.abr_enabled || input_para.vad_enabled))
	{
		fprintf(stderr, "Warning: --dtx is useless without --vad, --vbr or --abr\n");
	}
	else if ((input_para.vbr_enabled || input_para.abr_enabled) && (input_para.vad_enabled))
	{
		fprintf(stderr, "Warning: --vad is already implied by --vbr or --abr\n");
	}
	if (input_para.abr_enabled)
	{
		speex_encoder_ctl(st, SPEEX_SET_ABR, &(input_para.abr_enabled));
	}

	speex_encoder_ctl(st, SPEEX_SET_HIGHPASS, &(input_para.highpass_enabled));

	penc = (state_enc *)speex_alloc(sizeof(state_enc));
	if (!penc)
		return -1;

	/*Initial bits parameters*/
	pbits = (SpeexBits*)speex_alloc(sizeof(SpeexBits));
	if (!pbits)
		return -1;

	speex_bits_init(pbits);


    penc->codec_st = st;
	penc->bits = pbits;
	penc->Bits_buf_len = 0;
	penc->HisLen = 0;

	*enc = penc;

	return 0;
}


/*
This is the open function for speex decoder

INPUT:
		void *dec:   decoder state
OUTPUT:
		void *dec:   decoder state

HISTORY:
		Version No.  Author         Remarks
		v01       Yongtao Sha    Created on 2016-11-2
*/

int dec_open_func(state_dec **dec)
{
	state_dec *pdec;
	int modeID;
	void *st;
	const SpeexMode *mode = NULL;
	SpeexBits *pbits;
	dec_para input_para =
	{
		16000, // rate; //sampling rate
		1 // enh_enabled;//enable post-filter (default 1) 
		  //0, // quiet;//default 0
		  //1, // forceMode;//Force decoding in narrowband(0),wideband(1),ultra-wideband(2), default -1
		  //1, // channels;//Force decoding in mono(1),stereo(2), default 1
		  //-1 //loss_percent;//Simulate n % random packet loss, default -1
	};

	if (input_para.Fs == 8000)
		modeID = SPEEX_MODEID_NB;
	else if (input_para.Fs == 16000)
		modeID = SPEEX_MODEID_WB;
	else if (input_para.Fs == 32000)
		modeID = SPEEX_MODEID_UWB;
	else
	{
		return -1;
		fprintf(stderr, "Error: sampling rate %d is not suitable, please try 8000, 16000 or 32000\n", input_para.Fs);
	}

	mode = speex_lib_get_mode(modeID);

	/*Initialize Speex decoder*/
	st = speex_decoder_init(mode);
	if (!st)
	{
		fprintf(stderr, "Decoder initialization failed.\n");
		return -1;
	}

	speex_decoder_ctl(st, SPEEX_SET_ENH, &(input_para.enh_enabled));
	speex_decoder_ctl(st, SPEEX_SET_SAMPLING_RATE, &(input_para.Fs));

	pdec = (state_dec *)speex_alloc(sizeof(state_dec));
	if (!pdec)
		return -1;

	/*Initial bits parameters*/
	pbits = (SpeexBits*)speex_alloc(sizeof(SpeexBits));
	if (!pbits)
		return -1;

	speex_bits_init(pbits);

	pdec->codec_st = st;
	pdec->bits = pbits;

	pdec->output_buf_len = 0;

	*dec = pdec;

	return 0;
}


void enc_reset(void *enc)
{
	if (enc != NULL)
	{
		state_enc *penc = (state_enc *)enc;

		penc->HisLen = 0;
	}
	
}
/*
This is the process function for speex encoder

INPUT:		
		void *enc:        encoder state
		short *input_buf: input data
		int input_len:  input length
OUTPUT:
		void *enc:        encoder state
		char **cbits:     encoder bits

HISTORY:
		Version No.  Author         Remarks
		v01       Yongtao Sha    Created on 2016-11-2
*/
int enc_process_func(void *enc, short *input_buf, int input_len, char **cbits)
{
	int cbits_len = 0;
	short *pdata = input_buf;//pointer to the input
	state_enc *penc = (state_enc *)enc;	
	char *pOutBuf = NULL;
	int l_cbits = 0;
	SpeexBits *pbits = (SpeexBits *)(penc->bits);

	//output len according to input len with extra 1-frame because of history len may be none zero
	cbits_len = ((input_len) / FRAME_SIZE + 1)*CBITS_SIZE;
	if (penc->Bits_buf_len == 0)
	{
		*cbits = (char*)speex_alloc(sizeof(char)*cbits_len);
		if (!(*cbits))
			return -1;

		penc->cbits = (void*)(*cbits);
		penc->Bits_buf_len = cbits_len;
	}
	else if(penc->Bits_buf_len < cbits_len)
	{
		*cbits = (char*)speex_realloc((char *)(penc->cbits), sizeof(char)*cbits_len);
		if (!(*cbits))
			return -1;

		penc->cbits = (void*)(*cbits);
		penc->Bits_buf_len = cbits_len;
	}
	else
	{
		*cbits = (char *)(penc->cbits);		
	}

	//reset
	pOutBuf = (char *)(*cbits);//output buffer
	
	if (penc->HisLen > 0)
	{
		memcpy(penc->pHisBuf + penc->HisLen, input_buf, (FRAME_SIZE - penc->HisLen) * sizeof(short));
		speex_bits_reset(pbits);
		speex_encode_int(penc->codec_st, penc->pHisBuf, pbits);
		l_cbits = speex_bits_write(pbits, pOutBuf, CBITS_SIZE);
		

		input_len -= (FRAME_SIZE - penc->HisLen);
		pdata = input_buf + (FRAME_SIZE - penc->HisLen);

		cbits_len= CBITS_SIZE;
		pOutBuf = pOutBuf + CBITS_SIZE;

		penc->HisLen = 0;
	}
	else
	{
		pdata = input_buf;
		cbits_len = 0;
	}


	while (input_len >= FRAME_SIZE)
	{
		speex_bits_reset(pbits);
		speex_encode_int(penc->codec_st, pdata, pbits);
		l_cbits = speex_bits_write(pbits, pOutBuf, CBITS_SIZE);
		
		input_len -= FRAME_SIZE;
		pdata = pdata + FRAME_SIZE;

		cbits_len += CBITS_SIZE;
		pOutBuf = pOutBuf + CBITS_SIZE;
	}
	
	if (input_len > 0)
	{
		memcpy(penc->pHisBuf, pdata, input_len * sizeof(short));
		penc->HisLen = input_len;
	}

	return cbits_len;

}

/*
This is the process function for speex encoder

INPUT:
		void *dec:          decoder state
		char *cbits:        encoder bits
		int cbits_len:    encoder bits length
OUTPUT:
		void *dec:          decoder state
		short **output_buf: decoder output

HISTORY:
		Version No.  Author         Remarks
		v01       Yongtao Sha    Created on 2016-11-2
*/
int dec_process_func(void *dec, char *cbits, int cbits_len, short **output_buf)
{
	int output_len,ret;
	state_dec *pdec = (state_dec *)dec;
	SpeexBits *pbits = (SpeexBits *)(pdec->bits);
	int frame_num = (cbits_len - 1) / CBITS_SIZE + 1;
	char *pcbits = cbits;
	short *pout;

	output_len = frame_num*FRAME_SIZE;

	if (pdec->output_buf_len == 0)
	{
		*output_buf = (short*)speex_alloc(sizeof(short)*output_len);
		if (!(*output_buf))
			return -1;

		pdec->output_data = (void*)(*output_buf);
		pdec->output_buf_len = output_len;
		memset(pdec->output_data, 0, sizeof(short)*output_len);
	}
	else if (pdec->output_buf_len < output_len)
	{
		*output_buf = (short*)speex_realloc((short *)(pdec->output_data), sizeof(short)*output_len);
		if (!(*output_buf))
			return -1;

		pdec->output_data = (void*)(*output_buf);
		pdec->output_buf_len = output_len;

	}
	else
	{
		*output_buf = (short *)(pdec->output_data);
		memset(pdec->output_data, 0, sizeof(short)*output_len);
	}

	pout = (short *) (*output_buf);	

	while(frame_num)
	{
		speex_bits_reset(pbits);

		speex_bits_read_from(pbits, pcbits, CBITS_SIZE);

		ret = speex_decode_int(pdec->codec_st, pbits, pout);

		if ((ret == -1) || (ret == -2))
		{
			fprintf(stderr, "Decoding error: corrupted stream?\n");
			break;
		}
		pout = pout + FRAME_SIZE;
		pcbits = pcbits + CBITS_SIZE;
		frame_num--;
	}	

	return output_len;
}

/*
This is the close function for speex encoder

INPUT:
		void *enc: encoder state

OUTPUT:

HISTORY:
		Version No.  Author         Remarks
		v01       Yongtao Sha    Created on 2016-11-2
*/
void enc_close_func(void *enc)
{
	state_enc *penc = (state_enc *)enc;
	void *st = (void *)(penc->codec_st);
	SpeexBits *pbits = (SpeexBits *)(penc->bits);
	speex_encoder_destroy(st);
	speex_bits_destroy(pbits);
	free(penc->cbits);
	free(penc);
}


/*
This is the close function for speex decoder

INPUT:
		void *dec: decoder state

OUTPUT:

HISTORY:
		Version No.  Author         Remarks
		v01       Yongtao Sha    Created on 2016-11-2
*/
void dec_close_func(void *dec)
{
	state_dec *pdec = (state_dec *)dec;
	void *st = (void *)(pdec->codec_st);
	SpeexBits *pbits = (SpeexBits *)(pdec->bits);
	speex_decoder_destroy(st);
	speex_bits_destroy(pbits);
    free(pbits);
	free(pdec->output_data);
	free(pdec);
}

