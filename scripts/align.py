import argparse
import sys
#sys.path.append('/clwork/aizhan/nlu-MT-new/src')
import bert_tokenize


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--predict', type=str, required=True)
    parser.add_argument('--source', type=str, required=True)
    parser.add_argument('--bpe_source', type=str, required=True)
    parser.add_argument('--label', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--target_lang', type=str, required=True)

    args = parser.parse_args()

    return args


def align_source(orig_source, label, sys_source):
    if len(orig_source) == len(sys_source):
        return label

    idx = 0
    bpe_flag = False
    intent = label.pop(-1)
    new_label = []

    for token in sys_source:
        if '@@' in token:
            bpe_flag = True
            new_label.append(label[idx])
        else:
            if bpe_flag:
                bpe_flag = False
                new_label.append(label[idx])
                idx += 1
            else:
                if token == orig_source[idx]:
                    new_label.append(label[idx])
                    idx += 1
                else:
                    print('BAG')
                    print(orig_source)
                    print(sys_source)
                    print(token)
                    print(label[idx])
                    exit()

    new_label.append(intent)

    return new_label


def align_target(target, label):
    bpe_flag = False
    intent = label.pop(-1)
    new_target = []
    new_label = []

    for idx, token in enumerate(target):
        if '@@' in token:
            if not bpe_flag:
                # Use the label of the first token of bpe
                new_label.append(label[idx])
                new_target.append(token[:-2])
                bpe_flag = True
            else:
                new_target[-1] += token[:-2]
        else:
            if bpe_flag:
                bpe_flag = False
                new_target[-1] += token
            else:
                new_target.append(token)
                new_label.append(label[idx])

    if len(new_target) != len(new_label):
        print(target, len(target))
        print(label, len(label))
        print(new_target, len(new_target))
        print(new_label, len(new_label))
        exit()

    new_label.append(intent)

    return new_target, new_label


def main(args):

    predicts = []
    sys_sources = []
    aligns = []

    for l in open(args.predict):
        l = l.strip()
        if l.startswith('H'):
            l = l.split()[2:]
            predicts.append(l)
        elif l.startswith('A'):
            l = l.split()[1:]
            l = [ll.split('-')[0] for ll in l]
            aligns.append(l)

    sys_sources = [l.strip().split() for l in open(args.bpe_source)]
    orig_sources = [l.strip().split() for l in open(args.source)]
    orig_targets = [l.strip().split() for l in open(args.source)]
    orig_labels = [l.strip().split() for l in open(args.label)]

    aligned_labels = [align_source(o, l, s) for o, l, s in zip(orig_sources, orig_labels, sys_sources)]

    lw = open(f'{args.output}/sys_label.{args.target_lang}', 'w')
    tw = open(f'{args.output}/sys_text.{args.target_lang}', 'w')

    for os, ol, p, a, al in zip(orig_sources, orig_labels, predicts, aligns, aligned_labels):
        labels = []
        intent = al[-1]
        al = al[:-1]
        for idx in a:
            idx = int(idx)
            labels.append(al[idx])
        labels.append(intent)
        target, labels = align_target(p, labels)
        target = ' '.join(target)
        labels = ' '.join(labels)
        lw.write(f'{labels}\n')
        tw.write(f'{target}\n')


if __name__ == "__main__":
    args = parse_args()
    main(args)
