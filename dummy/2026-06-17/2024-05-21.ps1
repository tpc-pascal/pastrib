#!/bin/bash
pip install -r requirements.txt  # hy vọng không conflict

@echo off
echo Dang deploy...
npm run build
if %errorlevel% neq 0 (
    echo "Bug roi"
    pause
)

