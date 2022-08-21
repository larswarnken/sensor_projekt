class Data:
    loaded_sample_rate = 0
    loaded_record_time = 0
    loaded_data = []

    def read_data(self, path):
        # reads data from file
        with open(path, 'r') as file:
            details = file.read()
            x = details.split('\n')
        try:
            # saves info from first line
            self.loaded_sample_rate = int(x[0].split(", ")[0])
            self.loaded_record_time = int(x[0].split(", ")[1])
            # delete first line which is samlpe rate and time
            x.pop(0)
            # adds data to list
            self.loaded_data = []
            for i in x:
                if i != '':
                    self.loaded_data.append(float(i))
        except:
            print("reading error")

