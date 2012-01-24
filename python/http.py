import httplib

def main():
    conn = httplib.HTTPSConnection('www.google.com')
    conn.request('GET', '/')
    response = conn.getresponse()

    print(response.status, response.reason)
    print('Headers:', response.getheaders())
    print('Data:', response.read())

    conn.close()

if __name__ == '__main__':
    main()
