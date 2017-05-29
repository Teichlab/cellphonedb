def remove_not_defined_columns(data_frame, defined_columns):
    data_frame_keys = data_frame.keys()

    for key in data_frame_keys:
        if key not in defined_columns:
            data_frame.drop(key, axis=1, inplace=True)

    return data_frame