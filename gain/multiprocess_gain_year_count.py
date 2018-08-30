import multiprocessing
import utilities
import create_gain_year_count

# Location of the carbon pools
carbon_pool_dir = 's3://gfw2-data/climate/carbon_model/carbon_pools/20180815'

# Loss, gain, and tree cover density tiles
loss = 's3://gfw2-data/forest_change/hansen_2015/Loss_tiles/'
gain = 's3://gfw2-data/forest_change/tree_cover_gain/gaindata_2012/'
tcd = 's3://gfw2-data/forest_cover/2000_treecover/'

# carbon_tile_list = utilities.tile_list('{}/carbon/'.format(carbon_pool_dir))
carbon_tile_list = ["00N_050W", "00N_060W"]
# carbon_tile_list = ['00N_050W'] # test tile
print carbon_tile_list

# utilities.s3_folder_download('{}'.format(loss), '.')
# utilities.s3_folder_download('{}'.format(gain), '.')
# utilities.s3_folder_download('{}'.format(tcd), '.')

for tile in carbon_tile_list:

    utilities.s3_file_download('{0}{1}.tif'.format(loss, tile), '.')
    utilities.s3_file_download('{0}Hansen_GFC2015_gain_{1}.tif'.format(gain, tile), '.')
    utilities.s3_file_download('{0}Hansen_GFC2014_treecover2000_{1}.tif'.format(tcd, tile), '.')

# if __name__ == '__main__':
#
#     count = multiprocessing.cpu_count()
#     pool = multiprocessing.Pool(processes=2)
#     pool.map(create_gain_year_count.create_gain_year_count, carbon_tile_list)

# for tile in carbon_tile_list:
#
#     create_gain_year_count.create_gain_year_count(tile)