#!/bin/bash
curl -X POST -H "Content-Type: application/json" -d '{"sensoryLoad":50,"cognitiveLoad":50,"workHours":50,"sleepQuality":50,"hyperfocusTime":50,"maskingLevel":50,"riskPercentage":50}' https://neurovibe.se/api/burnout-data
