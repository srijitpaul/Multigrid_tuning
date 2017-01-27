#!/bin/bash -l

filelocation=$1

filename=$2

block_0_L=$3

block_0_T=$4

block_1_L=$5

block_1_T=$6

sed '17s/.*/block ={'$block_0_L', '$block_0_L', '$block_0_L', '$block_0_T'}/' dummy_d7.qlua > test1.qlua
sed '18s/.*/block_1 ={'$block_1_L', '$block_1_L', '$block_1_L', '$block_1_T'}/' test1.qlua > test2.qlua

cp test2.qlua $filelocation/$filename.qlua
rm test1.qlua
rm test2.qlua
