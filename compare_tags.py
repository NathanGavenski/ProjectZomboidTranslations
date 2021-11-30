import argparse
from os import listdir
from os.path import isfile

def get_args():
    '''
        Arguments for comparing tags between languages.
    '''
    parser = argparse.ArgumentParser(description='Args for comparing tags')
    parser.add_argument('--origin', default='EN', help='Which language should it compare to')
    parser.add_argument('--destiny', default='PTBR', help='Which language should it compare with')
    return parser.parse_args()

if __name__ == '__main__':
    '''
        This function will compare tags from translation files from two different languages.
        This only use python default packages so no extra instalations are required.

        For running just execute:
        python compare_tags.py --origin EN --destiny PTBR
    '''
    args = get_args()
    english_path = f'./{args.origin}'
    english_files = [f'{english_path}/{f}' for f in listdir(english_path) if isfile(f'{english_path}/{f}')]
    english_files.sort()

    count = 0
    with open('tag_difference.txt', 'w') as result:
        for en_file in english_files:

            trans_file = en_file.replace(args.origin, args.destiny)

            en_dict = {}
            with open(en_file, 'r') as f:
                for line in f:
                    if "=" in line:
                        key_and_value = line.split(' = ')
                        if key_and_value[-1] != '{\n':
                            key = key_and_value[0].replace(' ', '').replace('\t', '')
                            value = key_and_value[-1]
                            en_dict[key] = value

            trans_dict = {}
            with open(trans_file, 'r') as f:
                for line in f:
                    if '=' in line:
                        key_and_value = line.split(' = ')
                        if key_and_value[-1] != '{\n':
                            key = key_and_value[0].replace(' ', '').replace('\t', '')
                            value = key_and_value[-1]
                            trans_dict[key] = value
            difference = list(set(en_dict.keys()).difference(list(trans_dict.keys())))

            if len(difference) > 0:
                result.write(f'{en_file} {trans_file} {difference}\n')
                count += len(difference)
    
        result.write(f'Difference: {count}')
