from room_reservator.test01.views import getRoomId
from django.shortcuts import render

def main():
    data = getRoomId()
    print(data.meetingroomloc)


if __name__ == '__main__':
    main()