# TODO need some error checking in here

# prepare test folder
test_folder=$(date +%s)_test
user=ludovico99
mkdir $test_folder
chown $user $test_folder

# pwd starts in the jit-bench folder
pushd ../..


# prepare test languages
apt-get update
apt install php-cli
apt install luajit
apt install lua-posix
apt install ruby

# no env :)
pip3 install numpy
pip3 install pandas

#-------------------------------------------------------------------- not mod --------------------------------------------------------------------

# #run test
# popd
# python3 jit_test_fine.py $test_folder/no_module.csv
# chown $user $test_folder/no_module.csv
# pushd ../..

#-------------------------------------------------------------------- zone sync --------------------------------------------------------------------

make EXTRA_CFLAGS=-DZONE_KERNEL_SYNC_CHECK
insmod hook.ko

# start agent
python3 user/agent_zone.py &
AGENT_PID=$!

#run test
popd
python3 jit_test_fine.py $test_folder/zone_sync.csv
chown $user $test_folder/zone_sync.csv
pushd ../..

# clean up
kill -9 $AGENT_PID
rmmod hook.ko

# #---------------------------------------------------------------------- page sync --------------------------------------------------------------------

# make 
# insmod hook.ko

# # start agent
# python3 user/agent_page.py &
# AGENT_PID=$!

# #run test
# popd
# python3 jit_test_fine.py $test_folder/page_sync.csv
# chown $user $test_folder/page_sync.csv
# pushd ../..

# # clean up
# kill -9 $AGENT_PID
# rmmod hook.ko


