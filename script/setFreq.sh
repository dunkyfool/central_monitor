#!/bin/bash

nvidia-settings -a "[gpu:${1}]/GPUPowerMizerMode=1"
nvidia-settings -a "[gpu:${1}]/GPUGraphicsClockOffset[1]=-200"
nvidia-settings -a "[gpu:${1}]/GPUMemoryTransferRateOffset[1]=${2}"
nvidia-settings -a "[gpu:${1}]/GPUFanControlState=1" 
nvidia-settings -a "[fan:${1}]/GPUTargetFanSpeed=80" 

