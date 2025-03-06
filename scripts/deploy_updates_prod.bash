docker system prune --force
cd /home/ubuntu/litebite
docker compose down
git fetch origin
git stash
git merge origin/main -m "merge with origin"
docker compose -f docker-compose-prod.yml up --build -d
