#!/bin/bash
# Installation directory
instDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $instDir
# Data directory - where files are stored
dataDir="$instDir"/data
# Output directory - tool output goes here
outDir="$instDir"/Output

# Output files for all tools
outFfmpeg=$outDir/ffmpeg.txt
outMediainfo=$outDir/mediainfo.txt
outPath=$outDir/path.txt

# Remove any old instances of output files and input dir-files
rm "$outDir"/*
while getopts "f:" arg; do
  case $arg in
    f) path=${OPTARG};
  esac
done
echo $path
echo -e "\e[1;31m Do you wanna delete previous data files before running integrity check? \e[0m"
read user_input
if [ $user_input == y ]; then
  echo "Removing..."
  rm $dataDir/*
fi
cp -t $dataDir $path/*  
for inputFile in $dataDir/*.wav; do
    echo "$inputFile" | sed "s/.*\///" >> $outFfmpeg  
    ffmpeg -v error -i $inputFile -f null - 2>> $outFfmpeg
    echo "" >> $outFfmpeg
    echo "$inputFile" | sed "s/.*\///" >> $outMediainfo
    mediainfo $inputFile -show_format -show_streams >> $outMediainfo
    echo "" >>$outMediainfo
done
python ./local_check.py
