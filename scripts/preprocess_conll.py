import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', type=str, required=True,
                        help='conll format')
    parser.add_argument('--text_output', type=str, required=True)
    parser.add_argument('--label_output', type=str, required=True)

    args = parser.parse_args()

    return args


def align(x, y, label):
    if len(x) == len(y):
        return label

    new_label = []
    idx = 0
    for token in y:
        if '@@' in token:
            bpe_flag = True
            new_label.append(label[idx])
        else:
            if bpe_flag:
                bpe_flag = False
                new_label.append(label[idx])
                idx += 1
            else:
                if token == x[idx]:
                    new_label.append(label[idx])
                    idx += 1

    return new_label


def main(args):
    text_fw = open(args.text_output, 'w')
    label_fw = open(args.label_output, 'w')

    data_l = []
    tmp_l = []

    for l in open(args.input):
        l = l.strip()
        if l.startswith('#'):
            pass
        elif len(l) == 0:
            data_l.append(tmp_l)
            tmp_l = []
        else:
            l = l.split('\t')
            tmp_l.append(l)

    for data in data_l:
        text = []
        label = []
        for l in data:
            text.append(l[1])
            label.append(l[3])
            intent = l[2]
        text = ' '.join(text)
        label = ' '.join(label)
        text_fw.write(text + '\n')
        label_fw.write(label + '\t' + intent + '\n')


if __name__ == "__main__":
    args = parse_args()
    main(args)
