export DB_NAME="spotify"
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=e2Qx9E3ifEmP2oiaHa4R
export POSTGRES_HOST=spotifydb.clm9mbbezu5l.us-east-1.rds.amazonaws.com

./create_table.sh
./populate.sh
./create_index.sh
