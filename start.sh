#!/bin/bash
cd backend && pip install -r requirements.txt & cd ..
echo Backend Ready!
cd frontend && npm install & cd ..
echo Frontend Ready!
python backend/app.py &
npm --prefix frontend start
