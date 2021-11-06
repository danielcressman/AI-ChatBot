import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean up data + model files in a directory')
    parser.add_argument('directory', metavar='DIR', type=str, help='the directory to clean up')
    args = parser.parse_args()
    directory = os.path.abspath(args.directory)

    files = ['checkpoint', 'data.pickle', 'model.tflearn.data-00000-of-00001', 'model.tflearn.index', 'model.tflearn.meta']
    for filename in files:
        path = os.sep.join([directory, filename])
        os.remove(path)
        print('Removed {}'.format(path))
