#!/bin/bash

nvidia-settings -a "[gpu:${1}]/GPUPowerMizerMode=1"
nvidia-settings -a "[gpu:${1}]/GPUGraphicsClockOffset[3]=-400"
nvidia-settings -a "[gpu:${1}]/GPUMemoryTransferRateOffset[3]=${2}"
nvidia-settings -a "[gpu:${1}]/GPUFanControlState=1" 
nvidia-settings -a "[fan:${1}]/GPUTargetFanSpeed=100" 

