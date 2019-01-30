from torch.utils.data import DataLoader

class NBADataloader(DataLoader):

    def __init__(self, *args, **kwargs):
        super(NBADataloader, self).__init__(*args, **kwargs)
