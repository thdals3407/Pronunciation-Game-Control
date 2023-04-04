def Mic_device_detector(audio):
    for index in range(audio.get_device_count()):
        desc = audio.get_device_info_by_index(index)
        device_list = []
        index_list = []
        print("DEVICE: {device}, INDEX: {index}".format(
            device=desc['name'], index=index))
        if "마이크" in desc['name'] or "mic" in desc['name']:
            device_list.append(desc['name'])
            index_list.append(index)
    for i in range(len(index_list)):
        print("DEVICE: {device}, INDEX: {index}".format(
            device=device_list[i], index=index_list[i]))
    return device_list, index_list