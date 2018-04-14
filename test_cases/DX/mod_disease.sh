#!/bin/bash 


cd /Users/abin-personal/Google\ Drive/1_MSTP/2_Research/1_CapraLab/courses/BMIF6315/assignments/clinical_decision_support/clin_decis_support_assignment

awk '/DX/{x="DX"++i;}{print > x;}' Diseases_for_2018_decision_support_exercise.txt

#remove LINK for all DX files in place
sed -i -e '/^LINK/d' DX* 