counter = 0


def find_dings(data_p, sample_rate_p):

    print('length data: ', len(data_p))

    if len(data_p) > 0:

        max_value = max(data_p)

        puffer_seconds = 1.5
        puffer_samples = round(puffer_seconds * sample_rate_p)

        trigger_value = max_value * 0.4

        global counter

        if len(data_p) > puffer_samples:

                for value in data_p:
                    if value >= trigger_value:
                        counter += 1

                        start_index = round(data_p.index(value) - sample_rate_p * 0.10)
                        end_index = start_index + puffer_samples

                        cut_data = data_p[start_index:end_index]

                        # if len(cut_data) == puffer_samples_p:
                        #     with open(f'Files/{filename_p}_{counter}.txt', 'w') as newfile:
                        #         newfile.write(f'{sample_rate_p}, {int(puffer_seconds_p*1000)}\n')
                        #         for e in cut_data:
                        #             newfile.write(f'{e}\n')
                        #
                        #     find_dings(filename_p, data_p[end_index:len(data_p)], max_value_p, sample_rate_p, puffer_samples_p, puffer_seconds_p)

                        print('length cut data: ', len(cut_data))

                        return cut_data
        else:
            return data_p
