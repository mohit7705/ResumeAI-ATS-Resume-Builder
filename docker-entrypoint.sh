#!/bin/sh
set -e

cd /app
mkdir -p data/personal data/projects generated/html generated/pdf generated/css generated/assets

seed() { [ -f "$1" ] || printf '%s\n' "$2" > "$1"; }
seed data/personal/profile.json        '{}'
seed data/personal/contact.json        '{}'
seed data/personal/skills.json         '{}'
seed data/personal/summary.json        '{"summary": ""}'
seed data/personal/education.json      '[]'
seed data/personal/experience.json     '[]'
seed data/personal/certifications.json '[]'
seed data/personal/achievements.json   '[]'
seed data/projects/projects.json       '[]'

exec "$@"
