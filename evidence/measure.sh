#!/bin/bash
cd ~/sqe/PX4-Autopilot || exit 1
[ -d build/px4_sitl_test ] || { echo "build dir missing - rebuild first"; exit 1; }
find build/px4_sitl_test -name '*.gcda' -delete
(cd build/px4_sitl_test && ctest --timeout 60 -R 'functional-ManualControlSQE|unit-ManualControlSelectorSQE' 2>&1 | grep -v px4_work_queue | tail -8)
lcov --directory build/px4_sitl_test --base-directory build/px4_sitl_test --gcov-tool gcov --capture \
  --rc branch_coverage=1 --rc geninfo_unexecuted_blocks=1 --ignore-errors mismatch,negative,gcov \
  -o coverage/lcov_own.info 2>&1 | tail -1
lcov --remove coverage/lcov_own.info '/usr/*' '*/build/*' '*/googletest/*' '*/boards/*' \
  --rc branch_coverage=1 --ignore-errors unused,mismatch,negative -o coverage/lcov_own_filtered.info 2>&1 | tail -1
echo "== baseline (upstream tests)"; python3 ~/sqe/file_cov.py coverage/lcov_filtered.info ManualControl.cpp ManualControlSelector.cpp
echo "== own tests";                 python3 ~/sqe/file_cov.py coverage/lcov_own_filtered.info ManualControl.cpp ManualControlSelector.cpp
python3 ~/sqe/uncovered.py ManualControl.cpp coverage/lcov_own_filtered.info > ~/sqe/evidence/test_logs/uncovered_ManualControl_latest.txt
mkdir -p ~/sqe/gcov_work && cd ~/sqe/gcov_work && rm -f *.gcov
OBJ=~/sqe/PX4-Autopilot/build/px4_sitl_test/src/modules/manual_control/CMakeFiles/modules__manual_control.dir/ManualControl.cpp.o
gcov -b -c -o $OBJ ~/sqe/PX4-Autopilot/src/modules/manual_control/ManualControl.cpp > gcov_stdout.txt 2>&1
python3 ~/sqe/classify.py ManualControl.cpp | tee ~/sqe/evidence/test_logs/branch_classification.txt
