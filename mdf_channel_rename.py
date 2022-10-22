"""
    This module will replace the channel names in _mdf_ files base on replacement dictionaries defined
    in csv (';') formats.
    - Multiple files could be to the argument list. 
    - The input dictionaries will be merged, 
    - input data files will be processed one-by-one.
"""
import logging
import time

import warningfilter
import sys
from pathlib import Path
from asammdf import MDF
import pandas as pd
from tqdm import tqdm


def parse_argv(argv):
    """
    Parse the command line argument vector
    :param argv: command line argument vector (list)
    :return: parsed arguments in separate variables
    """
    data_path_list = list()
    channel_name_path_list = list()
    option_dict = dict()

    for arg in argv:
        if '=' in arg:  # then it is an option
            option_dict.update({arg.split('=')[0]: arg.split('=')[1]})
        else:
            try:  # to treat as a path
                path = Path(arg)
                if path.suffix in ['.mf4', '.dat']:
                    data_path_list.append(path)
                if path.suffix in ['.txt', '.csv']:
                    channel_name_path_list.append(path)
            except:
                pass
    return data_path_list, channel_name_path_list, option_dict


def join_channel_name_sources(path_list):
    """
    Join the channel name replacement lists
    :param path_list: paths to the replacement lists
    :return: replacement dictionary
    """
    frame_list = []

    for filename in path_list:
        df = pd.read_csv(filename, sep=';', index_col=None, header=None)
        frame_list.append(df)

    try:
        frame = pd.concat(frame_list, axis=0, ignore_index=True)  # Concatenate lists
    except ValueError:
        print("There is no channel name dictionary defined.")
        exit(1)

    frame.drop_duplicates(inplace=True)  # Drop duplicated rows
    frame.dropna(inplace=True)  # Drop rows which has not filled
    frame.set_index(0, inplace=True)  # Prepare conversion to dictionary

    return frame.to_dict()[1]


if __name__ == '__main__':
    # Set logger
    LOG = logging.getLogger('console')
    logging.basicConfig(filename=f'{Path(__file__).stem}_{time.strftime("%Y%m%d-%H%M%S")}.log', level=logging.INFO)

    option_dict = {'new_fname_ext': '_renamed'}

    # Parse input arguments
    data_path_list, channel_name_path_list, option_dict_from_arg = parse_argv(sys.argv)
    option_dict.update(option_dict_from_arg)

    # Join channel name dictionaries
    channel_name_dict = join_channel_name_sources(channel_name_path_list)

    # Replace channel names in mdf files
    for mdf_path in tqdm(data_path_list):
        try:
            with MDF(mdf_path) as mdf:
                LOG.info(f'File opened: {mdf_path.name}')
                tqdm.write(f'File opened: {mdf_path.name}')

                for group in mdf.groups:
                    for channel in group.channels:
                        if channel.name in channel_name_dict.keys():
                            LOG.info(f'Channel name changes: {channel.name} -> {channel_name_dict[channel.name]} ')
                            tqdm.write(f'Channel name changes: {channel.name} -> {channel_name_dict[channel.name]} ')

                            channel.name = channel_name_dict[channel.name]

                mdf.save(mdf_path.stem + option_dict['new_fname_ext'] + mdf_path.suffix, compression=2)

        except FileNotFoundError:
            print(f"File not found: {mdf_path}")

    input('Press any key to end program...')
    print('Bye, have a beautiful time!')
