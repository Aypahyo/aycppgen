set -e
container=aycppgen_test
image=aycppgen:test
echo log > test.sh.log

docker build -t $image  . >> test.sh.log 2>&1
docker rm -f $container >> test.sh.log 2>&1 || true
echo run tests
docker run --name $container $image
docker logs $container >> test.sh.log 2>&1
docker rm -f $container >> test.sh.log 2>&1 || true
echo try install commands
docker run --entrypoint "/bin/bash" --name $container $image -c "pip install . && mkdir proj && cd proj && aycppgen --command selftest"
docker logs $container >> test.sh.log 2>&1
docker rm -f $container >> test.sh.log 2>&1 || true
