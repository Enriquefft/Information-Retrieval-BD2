aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/v5d5g0j4
docker build -t information_retreival_repo .
docker tag information_retreival_repo:latest public.ecr.aws/v5d5g0j4/information_retreival_repo:latest
docker push public.ecr.aws/v5d5g0j4/information_retreival_repo:latest
