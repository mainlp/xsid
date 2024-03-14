import argparse
import random
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results1", "-1", help="path to results of system1")
    parser.add_argument("--results2", "-2", help="path to results of system2")
    parser.add_argument("--resamples", "-r", type=int, default=1000, help="amount of resamples to use")
    parser.add_argument("--randseed", default=None, type=int, help="random seed, default=None")
    args = parser.parse_args()
    results = readResults([args.results1, args.results2])
    p = getP(results, args.resamples, args.randseed)
    print('p = {:.3f}'.format(p))

def readResults(paths):
    results = []
    #print('Loading...', file=sys.stderr)
    for system in paths:
        sys_results = []
        results.append(sys_results)
        try:
            with open(system) as res_file:
                sys_results.extend([float(l.strip()) for l in res_file])
        except FileNotFoundError:
            logging.warning(filename + ' not found')
    samples = len(sys_results)
    return results

# insert results as two dimensional list: a list of lists of scores
def getP(results, resamples=10000, randseed=None):
    if len(set([len(x) for x in results])) != 1:
        print('Error, results have different lengths: ', [len(x) for x in results])
        exit(1)
        
    if randseed != None:
        random.seed(randseed)
    samples = len(results[0])
    

    #print('Resampling...', file=sys.stderr)
    boot_results = []
    for i_resample in range(resamples):
        #print(i_resample + 1, file=sys.stderr, end='\r')
        resample_results = []
        boot_results.append(resample_results)
        for i_system in range(len(results)):
            sumScores = 0
            for _ in range(samples):
                sumScores += random.choice(results[i_system])
            resample_results.append(sumScores/samples)
    #print('\n', file=sys.stderr)
    # when comparing 2 systems, with resampling of 1000
    # boot_results = list of size 1000
    # in boot results, list of resample results of size 2= the average f1 of both systems
    # average is taken over `samples` instances, which is the total number of instances

    sys_fscores = []
    for i_system in range(len(results)):
        sys_fscores.append([boot_results[i_resample][i_system] for i_resample in range(resamples)])

    #final_results = []
    sys_sys_wins = [[0] * len(results) for x in range(len(results))]
    for i_system in range(len(results)):
        for j_system in range(i_system):
            for i, j in zip(sys_fscores[i_system], sys_fscores[j_system]):
                if i > j:
                    sys_sys_wins[i_system][j_system] += 1
                elif i < j:
                    sys_sys_wins[j_system][i_system] += 1
    # sys_sys_wins: matrix of (len(systems), len(systems)), containing number of wins

    team1avg = sum(sys_fscores[0]) / len(sys_fscores[0])
    team2avg = sum(sys_fscores[1]) / len(sys_fscores[1])
    if team1avg >= team2avg:
        return (sys_sys_wins[1][0] + 1) / (resamples + 1)
    else:
        return (sys_sys_wins[0][1] + 1) / (resamples + 1)

if __name__ == "__main__":
    main()


