import pandas

def FWHM(flag, sample_ID, input_df):

    if flag == 'pl':
        sample_params = []

        local_max = input_df.max()

        max_location = input_df.loc[input_df['counts'] == local_max['counts']]
        current_index = max_location.index

        # Check for halfpoint to the left of max
        while (input_df.iloc[current_index]['counts'].item() > (local_max['counts'] / 2)):
            current_index -= 1
        
        left_bound = input_df.iloc[current_index]

        current_index = max_location.index

        # Check for halfpoint to the right of max
        while (input_df.iloc[current_index]['counts'].item() > (local_max['counts'] / 2)):
            current_index += 1

        right_bound = input_df.iloc[current_index]

        fwhm = right_bound['wavelength'].item() - left_bound['wavelength'].item()

        sample_params = [
            sample_ID,
            max_location['wavelength'].item(),
            local_max['counts'],
            fwhm,
        ]

        return sample_params