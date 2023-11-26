aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 216144596950.dkr.ecr.us-east-1.amazonaws.com
docker build -t information_retreival_service .
docker tag information_retreival_service:latest 216144596950.dkr.ecr.us-east-1.amazonaws.com/information_retreival_service:latest
docker push 216144596950.dkr.ecr.us-east-1.amazonaws.com/information_retreival_service:latest
