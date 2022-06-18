#!/bin/bash

today=$(date)
finame="container_log"

fn="$finame $today"
fn+=".txt"

sudo docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" > /home/cutlets/dp/log/"$fn"

exit 0
