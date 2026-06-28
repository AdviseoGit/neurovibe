#!/bin/bash
curl -X POST -H "Content-Type: application/json" -d '{"sensoryLoad":8,"cognitiveLoad":7,"workHours":45,"sleepQuality":3,"hyperfocusTime":6,"maskingLevel":9,"riskPercentage":85}' https://neurovibe.se/api/burnout-data
