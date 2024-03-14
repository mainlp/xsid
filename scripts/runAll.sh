function run {
    $1 > $2.sh
    chmod +x $2.sh
    ./$2.sh
    # For slurm
    # python3 mtp/scripts/slurm.py $2.sh $2 20 > startSlurm.sh
    # chmod +x startSlurm.sh
    # ./startSlurm.sh
    # To run parallel on 1 machine (will give issues with gpus)
    # parallel -j 8 < $2.sh
}

./scripts/0.setup.sh
./scripts/0.udCollect.sh
python3 scripts/0.mtCollect.py

run "python3 scripts/1.mt.prep.py" "1.prep"
run "python3 scripts/1.mt.train.py" "1.train"
run "python3 scripts/1.mt.predict.py" "1.predict"
rm predictions/*eval
run "python3 scripts/1.mt.eval.py" "1.eval"

run "python3 scripts/2.mach.train.py" "2.train"
run "python3 scripts/2.mach.pred.py" "2.pred"
python3 scripts/2.mach.eval.py

run "python3 scripts/4.test.train.py" "4.train"
run "python3 scripts/4.test.pred.py" "4.pred"
rm predictions/test*eval
python3 scripts/4.test.eval.py


