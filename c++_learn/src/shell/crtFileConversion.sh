#!/bin/sh

#读文件ca-certificates.crt中-----BEGIN CERTIFICATE-----和-----END CERTIFICATE-----之间的内容并且要包含这两行内容，对每一项这样的
#内容执行 openssl x509 -in /file.crt -text
function read_dir(){
for file in `ls $1` #注意此处这是两个反引号，表示运行系统命令
	do
		if [ -d $1"/"$file ] #注意此处之间一定要加上空格，否则会报错
		then
		read_dir $1"/"$file
		else
		echo $1"/"$file #在此处处理文件即可
		fi
	done
}
