### This

import utilities
import datetime
import numpy as np
import rasterio

np.set_printoptions(threshold=np.nan)

def annual_gain_rate(tile_id, gain_table_dict):

    # upload_dir = 's3://gfw2-data/climate/carbon_model/forest_age_category/20180921/'
    upload_dir = r'C:\GIS\Carbon_model\test_annual_gain_rate'

    # Converts the forest age category decision tree values to the three age categories.
    # 10000: primary forest; 20000: secondary forest > 20 years; 30000: secondary forest <= 20 years
    # These are five digits so they can easily be added to the four digits of the continent-ecozone code to make unique codes
    # for each continent-ecozone-age combination.
    age_dict = {0: 0, 1: 20000, 2: 20000, 3: 10000, 4: 30000, 5: 20000, 6: 10000, 7: 30000, 8: 30000, 9: 30000, 10: 30000}

    print "Processing:", tile_id

    # start time
    start = datetime.datetime.now()

    # Names of the forest age category and continent-ecozone tiles
    age_cat = 'forest_age_category_{}.tif'.format(tile_id)
    cont_eco = 'fao_ecozones_continents_{}.tif'.format(tile_id)

    print "  Reading input files and evaluating conditions"

    # Opens biomass tile
    with rasterio.open(cont_eco) as cont_eco_src:

        # Grabs metadata about the tif, like its location/projection/cellsize
        kwargs = cont_eco_src.meta

        # Grabs the windows of the tile (stripes) so we can iterate over the entire tif without running out of memory
        windows = cont_eco_src.block_windows(1)

        # Opens gain tile
        with rasterio.open(age_cat) as age_cat_src:

            # Updates kwargs for the output dataset
            kwargs.update(
                driver='GTiff',
                count=1,
                compress='lzw',
                nodata=0,
                dtype='float32'
            )

            # Opens the output tile, giving it the arguments of the input tiles
            with rasterio.open('annual_gain_rate_{}.tif'.format(tile_id), 'w', **kwargs) as dst:

                # Iterates across the windows (1 pixel strips) of the input tile
                for idx, window in windows:

                    # Creates windows for each input raster
                    cont_eco = cont_eco_src.read(1, window=window)
                    age_cat = age_cat_src.read(1, window=window)

                    age_recode = np.vectorize(age_dict.get)(age_cat)

                    cont_eco_age = cont_eco + age_recode

                    cont_eco_age = cont_eco_age.astype('float32')

                    for k,v in gain_table_dict.iteritems():
                        cont_eco_age[cont_eco_age == k] = v

                    dst_data = cont_eco_age

                    # Writes the output window to the output
                    dst.write_band(1, dst_data, window=window)

    pattern = 'annual_gain_rate'

    utilities.upload_final(pattern, upload_dir, tile_id)

    end = datetime.datetime.now()
    elapsed_time = end-start

    print "  Processing time for tile", tile_id, ":", elapsed_time




