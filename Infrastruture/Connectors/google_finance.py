import urllib.request

def get_token():
    pass


def connect():
    url = 'https://www.google.com/search?site=finance&tbm=fin&q=INDEXDJX:+.DJI&stick=H4sIAAAAAAAAAONgecRozC3w8sc9YSmtSWtOXmNU4eIKzsgvd80rySypFBLjYoOyeKS4uDj0c_UNkgsry3kAQ0pLYDgAAAA&sa=X&ved=0ahUKEwi8lOaJz-_eAhVKXbwKHSKJDo0Q0uIBCKYBMBI&biw=1536&bih=763#scso=_d5_6W7XoLouE8gWng7mIDg2:0'
    data = urllib.request.urlopen(url).read()
    print(data)


if __name__ == '__main__':
    connect()